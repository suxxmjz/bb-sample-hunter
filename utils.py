import re
from typing import Tuple

def extract_artist_and_song(full_text: str) -> Tuple[str, str]:
    clean_text = re.sub(r'^\d+\.\s*', '', full_text) #filter out leading number and period, ex 300. song title

    if "“" in clean_text and "”" in clean_text: # ex: "New Kids on the Block, “You Got It (The Right Stuff)”"
        parts = clean_text.split(", “")
        if len(parts) > 1:
            artist = parts[0].strip()
            song_info = parts[1]
            split_song_info = song_info.split("”")
            song_name = split_song_info[0]
            song = song_name.strip()
            return artist, song

    return "ERROR", "Extracted: " + (clean_text)
