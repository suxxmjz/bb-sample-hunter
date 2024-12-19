import requests
from dotenv import load_dotenv
import os

BASE_URL = "https://api.genius.com"
load_dotenv()

ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

def search_song(song_title, logger):
    url = f"{BASE_URL}/search"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"q": song_title}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()["response"]["hits"]
        if results:
            return results[0]["result"]
        else:
            logger.error(f"Song not found for: {song_title}")
            return None
    else:
        logger.error(f"Error: {response.status_code} for song {song_title}")
        return None

def get_song_details(song_id, logger):
    url = f"{BASE_URL}/songs/{song_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["response"]["song"]
    else:
        logger.error(f"Error: {response.status_code} for song ID {song_id}")
        return None

def find_samples(artist, song_title, logger):
    full_query = f"{artist} {song_title}"
    song = search_song(full_query, logger)
    
    if not song:
        logger.error(f"Song not found for: {full_query}")
        return []
    
    song_id = song["id"]
    song_details = get_song_details(song_id, logger)
    
    if not song_details:
        logger.error(f"Could not retrieve song details for: {full_query}")
        return []

    samples = None
    for relationship in song_details.get("song_relationships", []):
        if relationship.get("relationship_type") == "samples":
            samples = relationship.get("songs", [])
            break
    
    if samples:
        return [sample.get("full_title") for sample in samples]
    
    return []
