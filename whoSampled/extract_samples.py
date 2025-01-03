from bs4 import BeautifulSoup
from typing import Tuple

def extract_extra_samples_from_html(html_content: str) -> Tuple[str, bool]:
    soup = BeautifulSoup(html_content, 'html.parser')
    sampled_songs = []

    sample_rows = soup.select("table.tdata tbody tr")

    for row in sample_rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            song_name = cells[1].find('a').text.strip()
            artist = cells[2].text.strip()
            sampled_songs.append(f"[{song_name} by {artist}]")

    return ', '.join(sampled_songs), False


def extract_samples_from_html(html_content: str, extraSamples: bool = False) -> Tuple[str, bool]:
    if extraSamples == True:
        return extract_extra_samples_from_html(html_content)


    soup = BeautifulSoup(html_content, 'html.parser')
    subsections = soup.find_all('section', class_='subsection')

    sampled_songs = []

    for subsection in subsections:
        header = subsection.find('header', class_='sectionHeader')
        if header and "Contains samples of" in header.text:
            see_all_button = subsection.find('a', class_='btn', text='see all')
            if see_all_button:
                return "See all button found, need to make additional request.", True
            table = subsection.find('table', class_='table tdata')
            if table:
                rows = table.find_all('tr')

                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) > 0:
                        song_name = cells[1].find('a').text.strip()
                        artist = cells[2].text.strip()
                        sampled_songs.append(f"[{song_name} by {artist}]")

    if not sampled_songs:
        return "No samples found.", False
    
    return ', '.join(sampled_songs), False
