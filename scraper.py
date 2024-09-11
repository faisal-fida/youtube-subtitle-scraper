import requests
import logging
import time
import re

from config import URL, HEADERS, JSON_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_request():
    """Send a POST request to the API endpoint and return the response data."""
    try:
        for attempt in range(3):
            response = requests.post(
                URL + "/action/extract", headers=HEADERS, json=JSON_DATA
            )
            if response.status_code == 200:
                print(response.text)
                return response.json()
            else:
                logger.warning(
                    f"Attempt {attempt+1} failed with status code {response.status_code}. Retrying..."
                )
                time.sleep(1)  # wait for 1 second before retrying
        logger.error("All attempts failed. Giving up.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None


def clean_subtitle_text(text):
    """Clean the subtitle text by removing newlines, extra spaces, and special characters."""
    text = re.sub(r"\s+", " ", text).strip()  # remove extra spaces
    text = re.sub(r"[^a-zA-Z0-9\s.,']", "", text)  # remove special characters
    return text


def get_subtitle_text(subtitle_url: str):
    """Get the text content of the subtitle file."""
    try:
        logger.info(f"Getting subtitle text from {subtitle_url}")
        response = requests.get(subtitle_url)
        if response.status_code == 200:
            subtitle_text = clean_subtitle_text(response.text)
            return subtitle_text
        else:
            logger.error(
                f"Failed to get subtitle text. Status code: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None


def parse_response(response_data):
    """Parse the response data and return the subtitle URL."""

    subtitle_urls = response_data.get("formats", {})
    print(response_data)

    if len(subtitle_urls) > 0:
        subtitle_url = subtitle_urls[0].get("url")
        if subtitle_url:
            subtitle_url = URL + subtitle_url + "?ext=txt"
            subtitle_text = get_subtitle_text(subtitle_url)
            if subtitle_text:
                yt_data = {
                    "title": response_data.get("title", None),
                    "duration": response_data.get("duration", None),
                    "uploader": response_data.get("uploader", None),
                    "subtitles": subtitle_text,
                }
                return yt_data
            else:
                logger.error("The subtitle text is empty")
                return None
        else:
            logger.error("There is no subtitle URL in the subtitle URLs list")
            return None
    else:
        logger.error("There are no subtitle URLs in the response data")
        return None


def run_scraper(yt_url: str):
    """Run the scraper with the given YouTube URL."""

    logger.info(f"Running scraper for {yt_url}")
    JSON_DATA["data"]["url"] = yt_url

    response_data = send_request()

    if not response_data:
        logger.error("Failed to get response data")
        return

    yt_data = parse_response(response_data.get("response", {}))

    if yt_data:
        logger.info(f"Successfully scraped data for {yt_url} - {yt_data.keys()}")
        return yt_data
    else:
        logger.error(f"Failed to scrape data for {yt_url}")
