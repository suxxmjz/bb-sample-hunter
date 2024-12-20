from typing import List
import pandas as pd
from genius_api import find_samples
from scraper import fetch_and_parse_html


def process_and_save_data(urls: List[str], output_csv: str, logger, processed_count: List[int]) -> bool:

    all_data = pd.DataFrame(columns=["Artist", "Song", "Samples"])
    
    try:
        for url in urls:
            try:
                parsed_data = pd.DataFrame(fetch_and_parse_html(url, logger, processed_count)) 
                
                if not parsed_data.empty:
                    samples_list = []
                    for _, row in parsed_data.iterrows():
                        artist = row["Artist"]
                        song = row["Song"]
                        
                        samples = find_samples(artist, song, logger)
                        if samples:
                            formatted_samples = "[" + "],[".join(samples) + "]"
                        else:
                            formatted_samples = "No samples found"
                        
                        samples_list.append(formatted_samples)
                    parsed_data["Samples"] = samples_list
                    
                    all_data = pd.concat([all_data, parsed_data], ignore_index=True)
                    logger.info(f"Processed data from URL: {url}")
            
            except Exception as e:
                logger.error(f"Error processing URL {url}: {e}")
                return False 

        all_data.to_csv(output_csv, index=False, encoding="utf-8-sig")
        logger.info(f"Data saved to {output_csv}")
        logger.info(f"Total songs processed: {processed_count[0]}")
        
    
    except Exception as e:
        logger.error(f"Critical error during processing: {e}")