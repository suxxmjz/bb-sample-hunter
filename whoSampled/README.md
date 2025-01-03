# Hunt for Samples in BB 500 List

## Goal:
Find samples used in the songs from [Billboard's 500 Best Pop Songs](https://www.billboard.com/lists/best-pop-songs-all-time-hits/irene-cara-flashdance-what-a-feeling/) into a formatted document (CSV), using WhoSampled as the sample source.

## To Run:
1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment (Windows)**:
     ```bash
     .\venv\Scripts\activate
     ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Convert `example.env` to `.env` and add the ScrapingBee API Key**
   - Refer to the [ScrapingBee Documentation](https://www.scrapingbee.com/documentation/#api_key) for more details.
   - Open the `.env` file and add your ScrapingBee API key:
     ```env
     SCRAPINGBEE_API_KEY=your_api_key
     ```
     
5. **Run the main script**:
   ```bash
   python main.py
   ```

## Tools Used:
- **Python**: The programming language.
- **Libraries**:
  - `scrapingbee`: To use ScrapingBee to access pages.
  - `beautifulsoup4`: For scraping and parsing HTML.
  - `python-dotenv`: To securely load API token.
  - `logging`: To keep track of what's happening and catch errors.

## How It Works:
1. **Read in CSV**:
   - The all_songs.csv is read in to extract the song and artists from the Billboard list.

2. **Extract Samples**:
   - A url is crafted to query WhoSampled using `scrapingbee` and an access token to find samples.
   - The HTML response is scraped using `beautifulsoup`, and the samples are appended to a list of dicts, which are written into an CSV.

4. **Logging**:
   - Python’s `logging` module logs actions and errors, so it's clear what's going on and troubleshooting is easier if needed.

## Flow:
1. **Input**: CSV of songs found from the Billboard 500 List (code in the main repo folder).
2. **Scraping**: For each song, scrape and parse the song samples.
3. **Output**: Save the song and sample data to an CSV file.
