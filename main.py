import logging
from data_processing import process_and_save_data

def setup_logger(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

def main():
    log_file = "app.log"
    logger = setup_logger(log_file)
    
    urls = [
        "https://www.billboard.com/lists/best-pop-songs-all-time-hits/100-del-shannon-runaway-2/",
        "https://www.billboard.com/lists/best-pop-songs-all-time-hits/200-van-halen-jump/",
        "https://www.billboard.com/lists/best-pop-songs-all-time-hits/annie-lennox-walking-on-broken-glass/",
        "https://www.billboard.com/lists/best-pop-songs-all-time-hits/belinda-carlisle-heaven-is-a-place-on-earth/",
        "https://www.billboard.com/lists/best-pop-songs-all-time-hits/"
    ]
    
    output_csv = "bb_with_samples.csv"
    
    res = process_and_save_data(urls, output_csv, logger, [0])
    if res:
        logger.info("All data processed successfully!")
    else:
        logger.error("Error processing data")

if __name__ == "__main__":
    main()
