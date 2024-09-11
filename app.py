from scraper import run_scraper

yt_url = "https://www.youtube.com/watch?v=3ckGtkuflsM"

yt_data = run_scraper(yt_url)

if yt_data:
    print(yt_data)
