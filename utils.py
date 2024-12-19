import re
import html

def extract_artist_and_song(full_text):
    clean_text = re.sub(r'^\d+\.\s*', '', full_text)
    clean_text = html.unescape(clean_text)

    if "—" in clean_text or "–" in clean_text:
        return map(str.strip, clean_text.split("—", 1))
    elif "“" in clean_text and "”" in clean_text:
        parts = clean_text.split(", “")
        if len(parts) > 1:
            artist = parts[0].strip()
            song = parts[1].split("”")[0].strip()
            return artist, song

    return "Unknown", clean_text
