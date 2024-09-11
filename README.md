# YouTube Subtitle Scraper

This project is a YouTube subtitle scraper that extracts subtitle text from YouTube videos. It sends a POST request to savesubs.com api.

## Features

- Sends POST requests to an API endpoint to extract subtitle URLs.
- Cleans subtitle text by removing newlines, extra spaces, and special characters.
- Handles retries and logs errors for failed requests.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/faisal-fida/youtube-subtitle-scraper.git
    ```
2. Navigate to the project directory:
    ```sh
    cd youtube-subtitle-scraper
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the scraper by executing the `app.py` file:
    ```sh
    python app.py
    ```
3. The script will print the scraped data, including the title, duration, uploader, and cleaned subtitles.

## Example

```python
from scraper import run_scraper

yt_url = "https://www.youtube.com/watch?v=3ckGtkuflsM"

yt_data = run_scraper(yt_url)

if yt_data:
    print(yt_data)
```

## Logging

The scraper uses Python's built-in `logging` module to log information, warnings, and errors. Logs are printed to the console for easy debugging.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.































































