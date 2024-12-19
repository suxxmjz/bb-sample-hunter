!Billboard Sample Hunter

# Billboard Sample Hunter

## Goal:
Find samples used in the songs from [Billboard's 500 Best Pop Songs](https://www.billboard.com/lists/best-pop-songs-all-time-hits/irene-cara-flashdance-what-a-feeling/) into a formatted document (Excel).

## To Run:
```
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
   - The song and sample data are organized into a list of dictionaries.
   - `Pandas` converts this list into a DataFrame and saves it to an Excel file.

4. **Logging**:
   - Python’s `logging` module logs actions and errors, so it's clear what's going on and troubleshooting is easier if needed.

## Flow:
1. **Input**: Start with a list of Billboard URLs that have song names.
2. **Scraping**: For each URL, scrape and parse the song titles.
3. **API Request**: Search each song on the Genius API and check for samples.
4. **Output**: Save the song and sample data to an Excel file.
