import pandas as pd
from genius_api import find_samples
from scraper import fetch_and_parse_html

def process_and_save_data(urls, output_excel, logger, processed_count):
    all_data = []
    for url in urls:
        parsed_data = fetch_and_parse_html(url, logger, processed_count)
        
        for entry in parsed_data:
            artist = entry["Artist"]
            song_title = entry["Song"]
            samples = find_samples(artist, song_title, logger)
            
            if samples:
                sample_list = "[" + "],[".join(samples) + "]"
            else:
                sample_list = "No samples found"
            
            all_data.append({"Artist": artist, "Song": song_title, "Samples": sample_list})
            logger.info(f"Processed: {artist} - {song_title}")
    
    df = pd.DataFrame(all_data)
    df.to_excel(output_excel, index=False) #used excel for readability
    logger.info(f"Data saved to {output_excel}")
    logger.info(f"Total songs processed: {processed_count[0]}")
