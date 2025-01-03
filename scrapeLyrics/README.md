# Scrape Lyrics and Annotations for Songs in BB 500 List

## Goal:
Get the lyrics and annotations from [Billboard's 500 Best Pop Songs](https://www.billboard.com/lists/best-pop-songs-all-time-hits/irene-cara-flashdance-what-a-feeling/) into a formatted document (JSON), using Genius as the source.

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
     ```
     GENIUS_ACCESS_TOKEN=your_access_token_here
     ```
     
5. **Run the main script**:
   ```bash
   python scrape_lyrics.py
   ```

## Tools Used:
- **Python**: The programming language.
- **Libraries**:
  - `lyricsgenius`: Python interface to interact with the Genius API. Uses `beautifulsoup` under the hood.
  - `pandas`: To read in data.
  - `numpy`: For handling and saving data.
  - `python-dotenv`: To securely load API token.
  - `logging`: To keep track of what's happening and catch errors.

## How It Works:
1. **Read in CSV**:
   - The all_songs.csv is read in to extract the song and artists from the Billboard list.

2. **Scrape Lyrics and Annotations with Genius API**:
   - Use `lyricsgenius` to query a song. The song and its info is saved as an object. With the song ID, find all referents, which contains the annotations.
   - The song with its lyrics and annotations is saved as a custom-defined numpy data type object, which will get written into a JSON file.

3. **Logging**:
   - Python’s `logging` module logs actions and errors, so it's clear what's going on and troubleshooting is easier if needed.

## Flow:
1. **Input**: CSV of songs found from the Billboard 500 List (code in the main repo folder).
2. **Scraping**: For each song, extract the lyrics and respective annotations using the Genius API.
3. **Output**: Save the song, lyric and annotation data to a JSON file.
