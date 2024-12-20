import requests
from requests import codes
from bs4 import BeautifulSoup
from utils import extract_artist_and_song
from typing import List, Dict

def fetch_and_parse_html(url: str, logger, processed_count: List[int]) -> List[Dict[str, str]]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43" 
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == codes.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            return parse_html(soup, logger, processed_count)
        else:
            logger.error(f"Failed to fetch page. Status code: {response.status_code} for URL: {url}")
            return []
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return []

def parse_html(soup: BeautifulSoup, logger, processed_count: List[int]) -> List[Dict[str, str]]:
    list_items = soup.find_all("li", class_="pmc-fallback-list-item-wrap")
    parsed_data = []

    for item in list_items:
        h2_tag = item.find("h2")
        if h2_tag:
            full_text = h2_tag.text.strip()
            artist, song = extract_artist_and_song(full_text)
            parsed_data.append({"Artist": artist, "Song": song})
            logger.info(f"Scraped: {artist} - {song}")
            processed_count[0] += 1

    return parsed_data
