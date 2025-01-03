![image](https://github.com/user-attachments/assets/6c65d13b-f8fa-4cdb-a943-c28d46fb9a43)

# Billboard Sample Hunter

## Goal:
Find samples used in the songs from [Billboard's 500 Best Pop Songs](https://www.billboard.com/lists/best-pop-songs-all-time-hits/irene-cara-flashdance-what-a-feeling/) into a formatted document (CSV).

## Note:
 - To view the code for scraping samples using WhoSampled, please refer to the whoSampled folder.
 - To view the code for scraping lyrics and annotations, please refer to the scrapeLyrics folder.
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

4. **Convert `example.env` to `.env` and add the Genius API access token**
   - Refer to the [Genius API Documentation](https://docs.genius.com/) for more details.
   - Open the `.env` file and add your Genius API access token:
     ```env
     GENIUS_ACCESS_TOKEN=your_genius_access_token_here
     ```
     
5. **Run the main script**:
   ```bash
   python main.py
   ```

## Tools Used:
- **Python**: The programming language.
- **Libraries**:
  - `requests`: To make HTTP requests.
  - `beautifulsoup4`: For scraping and parsing HTML.
  - `pandas`: For handling and saving data.
  - `python-dotenv`: To securely load API token.
  - `logging`: To keep track of what's happening and catch errors.

## How It Works:
1. **Scraping Billboard**:
   - `requests` is used to get the HTML from Billboard's site.
   - `BeautifulSoup` helps parse the HTML and pull out song details (like artist and song title).

2. **Talking to Genius API**:
   - The song info is sent to the Genius API using `requests` and an access token to find samples.

3. **Processing the Data**:
   - The song and sample data are organized into a `Pandas` dataframe.

4. **Logging**:
   - Python’s `logging` module logs actions and errors, so it's clear what's going on and troubleshooting is easier if needed.

## Flow:
1. **Input**: Start with a list of Billboard URLs that have song names.
2. **Scraping**: For each URL, scrape and parse the song titles.
3. **API Request**: Search each song on the Genius API and check for samples.
4. **Output**: Save the song and sample data to an CSV file.
