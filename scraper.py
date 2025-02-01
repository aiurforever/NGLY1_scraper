import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

# User-Agent to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

SEARCH_QUERIES = [
    ("en", "site:bbc.com OR site:cnn.com OR site:theguardian.com NGLY1"),  # English
    ("es", "site:elpais.com OR site:clarin.com OR site:elmundo.es NGLY1"),  # Spanish
]

GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}&hl={lang}&num=10"

def fetch_news(query, lang):
    search_url = GOOGLE_SEARCH_URL.format(query=query, lang=lang)
    print(f"🔎 Searching: {search_url}")

    response = requests.get(search_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Error: Unable to fetch results (Status Code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.find_all("div", class_="tF2Cxc"):
        title_tag = result.find("h3")
        link_tag = result.find("a")

        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = link_tag["href"]
            date = datetime.now().strftime("%Y-%m-%d")
            results.append({"date": date, "title": title, "url": link, "language": lang})

    return results

def scrape_all():
    all_results = []

    for lang, query in SEARCH_QUERIES:
        try:
            results = fetch_news(query, lang)
            all_results.extend(results)
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"❌ Error scraping {lang}: {e}")

    df = pd.DataFrame(all_results)

    if df.empty:
        print("⚠ No data found, CSV will not be created.")
    else:
        df.to_csv("news_mentions.csv", index=False)
        print("✅ Data saved to news_mentions.csv")

def run_cli_mode():
    scrape_all()
    if not os.path.exists("news_mentions.csv"):
        print("❌ ERROR: news_mentions.csv was NOT created!")
    else:
        print("✅ news_mentions.csv is ready.")

if __name__ == "__main__":
    run_cli_mode()
