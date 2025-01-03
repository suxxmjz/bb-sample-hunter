import csv
import logging
from urllib.parse import quote
from fetch_url import fetch_url_scrapingbee
from extract_samples import extract_samples_from_html


logging.basicConfig(
    filename='samples.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


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

def create_whosampled_url(artist: str, song: str) -> str:
    lead_artist = get_lead_artist(artist)
    lead_artist = lead_artist.replace('’', "'")
    song = song.replace('’', "'")
    encoded_artist = quote(lead_artist.replace(' ', '-'))
    encoded_song = quote(song.replace(' ', '-'))
    return f"https://www.whosampled.com/{encoded_artist}/{encoded_song}/"


def write_errors(errors: list) -> None:
    with open('errors.csv', 'a', newline='', encoding='utf-8') as error_file:
        writer = csv.writer(error_file)
        if error_file.tell() == 0:
            writer.writerow(['Artist', 'Song', 'URL', 'Error Response'])
        writer.writerows(errors)


def write_samples(samples: list) -> None:
    with open('all_samples.csv', 'a', newline='', encoding='utf-8') as sample_file:
        writer = csv.writer(sample_file)

        if sample_file.tell() == 0:
            writer.writerow(['Artist', 'Song', 'Samples'])

        for sample in samples:
            artist = sample['artist']
            song = sample['song']
            sampled_songs = sample['sampled_songs']
            writer.writerow([artist, song, sampled_songs])


def process_songs() -> None:
    errors = []
    all_samples = []

    row_start = 0
    row_end = 499


    with open('all_songs.csv', 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)

        rows = list(reader)[row_start:row_end + 1]

        for row in rows:
            artist, song = row
            url = create_whosampled_url(artist, song)
            logging.info(f"Processing: {artist} - {song} | URL: {url}")

            html_content, err = fetch_url_scrapingbee(url)

            if not err:
                samples, extraSamples = extract_samples_from_html(html_content)
                if extraSamples:
                    html_content, err = fetch_url_scrapingbee(url+"samples/")

                    samples, extraSamples = extract_samples_from_html(html_content, extraSamples=True)

                if samples:
                    all_samples.append({
                        'artist': artist,
                        'song': song,
                        'sampled_songs': samples
                    })
                    logging.info(f"Done extracting samples for: {artist} - {song}")
                else:
                    logging.warning(f"Error extracting samples for: {artist} - {song}")
            else:
                logging.error(f"Failed to fetch HTML for: {artist} - {song}")
                errors.append([artist, song, url, err])

    if all_samples:
        write_samples(all_samples)
        logging.info(f"Samples saved to all_samples.csv.")

    if errors:
        write_errors(errors)
        logging.error(f"Errors recorded in errors.csv.")

    logging.info("Processing complete. Check 'all_samples.csv' and 'errors.csv' for results.")

if __name__ == "__main__":
    process_songs()
