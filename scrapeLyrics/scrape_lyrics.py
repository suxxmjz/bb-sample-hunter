import json
import logging
from lyricsgenius import Genius
from dotenv import load_dotenv
import os
from typing import Union
import requests
import pandas as pd
import random
import time
import numpy as np
load_dotenv()

ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
BASE_URL = "https://api.genius.com"

genius = Genius(ACCESS_TOKEN, timeout=60)
genius.verbose = False
genius.remove_section_headers = True

song_dtype = np.dtype([
    ('artist', 'O'),
    ('song_title', 'O'),
    ('lyrics', 'O'),
    ('annotations', 'O'),
    ('song_id', 'i4'),
    ('success', 'bool')
])

annotation_dtype = np.dtype([
    ('lyric_fragment', 'O'),
    ('annotation', 'O')
])

def setup_logger(log_file: str) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

def get_lead_artist(artist: str) -> str:
    if 'feat' in artist.lower():
        artist = artist.split(' feat')[0].strip()
    elif 'and the' in artist.lower():
        artist = artist.split(' and the')[0].strip()
    elif 'feat.' in artist.lower():
        artist = artist.split(' feat.')[0].strip()
    elif 'vs.' in artist.lower():
        artist = artist.split(' vs.')[0].strip()
    elif '&' in artist:
        artist = artist.split('&')[0].strip()
    return artist

def random_delay(attempt: int = 1, base_delay: int = 1, max_delay: int = 32) -> np.void:
    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
    jitter = random.uniform(0, 1)
    time.sleep(delay + jitter)

def get_song_id(song_title: str, logger) -> Union[int, None]:
    url = f"{BASE_URL}/search"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": song_title}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        
        results = response.json().get("response", {}).get("hits", [])
        if results:
            return results[0]["result"]["id"]
        else:
            logger.error(f"Song not found for: {song_title}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching song ID for {song_title}: {e}")
        return None

def search_song(artist: str, song_title: str, logger) -> Union[object, None]:
    try:
        if artist:
            song = genius.search_song(song_title, artist)
            if song:
                logger.info(f"Processing: {artist} - {song_title}")
                return song
        
        #if artist isn't directly found, try using lead artist
        lead_artist = get_lead_artist(artist) if artist else None
        if lead_artist:
            song = genius.search_song(song_title, lead_artist)
            if song:
                logger.info(f"Processing with lead artist: {lead_artist} - {song_title}")
                return song

        #fallback: search by song ID
        song_id = get_song_id(song_title, logger)
        if song_id:
            song = genius.search_song(song_id=int(song_id))
            if song:
                logger.info(f"Processing with song ID: {song_id}")
                return song
        
        logger.error(f"Song not found: {artist} - {song_title}")
        return None
    except Exception as e:
        logger.error(f"Error fetching song: {artist} - {song_title} | {e}")
        return None

def fetch_annotations(song_id: int, logger) -> np.ndarray:
    url = f"https://api.genius.com/referents"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {
        "song_id": song_id,
        "text_format": "plain"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        referents = data.get("response", {}).get("referents", [])

        annotations = np.zeros(len(referents), dtype=annotation_dtype)
        
        for i, referent in enumerate(referents):
            fragment = referent.get("fragment", "")
            annotations_data = referent.get("annotations", [])
            
            if annotations_data:
                annotation_body = annotations_data[0].get("body", {})
                annotations[i] = (fragment, annotation_body)
        
        logger.info(f"Found {len(annotations)} annotations for song ID {song_id}")
        return annotations
    except Exception as e:
        logger.error(f"Error fetching annotations for song ID {song_id}: {e}")
        return np.array([], dtype=annotation_dtype)

def fetch_lyrics_and_annotations(artist: str, song_title: str, logger) -> np.array:
    song = search_song(artist, song_title, logger)
    if not song:
        return np.array([(
            artist,
            song_title,
            None,
            np.array([], dtype=annotation_dtype),
            -1,
            False
        )], dtype=song_dtype)[0]
    
    lyrics = song.lyrics
    annotations = fetch_annotations(song.id, logger)
    
    return np.array([(
        artist,
        song_title,
        lyrics,
        annotations,
        song.id,
        True
    )], dtype=song_dtype)[0]

def process_csv_file_with_retries(csv_file: str, logger, max_retries: int = 3) -> np.ndarray:
    try:
        df = pd.read_csv(csv_file)
        songs_data = np.zeros(len(df), dtype=song_dtype)
        retry_queue = []

        for index, row in df.iterrows():
            artist_name = row['Artist']
            song_title = row['Song']
            random_delay()
            song_data = fetch_lyrics_and_annotations(artist_name, song_title, logger)
            if not song_data['success']:
                retry_queue.append((index, artist_name, song_title))
            else:
                songs_data[index] = song_data

        for attempt in range(max_retries):
            if not retry_queue:
                break

            logger.info(f"Retrying {len(retry_queue)} failed requests (Attempt {attempt + 1})")
            new_retry_queue = []

            for index, artist_name, song_title in retry_queue:
                random_delay(attempt=attempt)
                song_data = fetch_lyrics_and_annotations(artist_name, song_title, logger)

                if not song_data['success']:
                    new_retry_queue.append((index, artist_name, song_title))
                else:
                    songs_data[index] = song_data

            retry_queue = new_retry_queue
        if retry_queue:
            logger.error(f"Failed to fetch {len(retry_queue)} songs after {max_retries} attempts:")
            for _, artist_name, song_title in retry_queue:
                logger.error(f"{artist_name} - {song_title}")

        return songs_data

    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return np.array([], dtype=song_dtype)

def save_to_json(data: np.ndarray, output_file: str, logger) -> None:
    try:
        songs_list = []
        for song in data:
            song_dict = {
                'artist': str(song['artist']),
                'song_title': str(song['song_title']),
                'lyrics': song['lyrics'],
                'annotations': [],
                'song_id': int(song['song_id']),
                'success': bool(song['success']),
            }

            if isinstance(song['annotations'], np.ndarray) and song['annotations'].size > 0:
                song_annotations = []
                for annotation in song['annotations']:
                    annotation_entry = {
                        'lyric_fragment': str(annotation['lyric_fragment']),
                        'annotation': annotation['annotation'],
                    }
                    song_annotations.append(annotation_entry)
                song_dict['annotations'] = song_annotations

            songs_list.append(song_dict)

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump({'songs': songs_list}, file, ensure_ascii=False, indent=4)
        logger.info(f"Data saved to {output_file}")
    except Exception as e:
        logger.error(f"Failed to save to {output_file}: {e}")
if __name__ == "__main__":
    log_file = "lyrics_scrape.log"
    logger = setup_logger(log_file)
    
    songs_data = process_csv_file_with_retries("all_songs.csv", logger)
    save_to_json(songs_data, "lyrics_and_annotations.json", logger)