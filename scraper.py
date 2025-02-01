import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import sys
from datetime import datetime
import time
import random

# User-Agent to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Google search URLs for different languages and countries
SEARCH_QUERIES = [
    ("en", "site:bbc.com OR site:cnn.com OR site:theguardian.com NGLY1"),  # English
    ("es", "site:elpais.com OR site:clarin.com OR site:elmundo.es NGLY1"),  # Spanish
    ("fr", "site:lemonde.fr OR site:lefigaro.fr OR site:liberation.fr NGLY1"),  # French
    ("de", "site:spiegel.de OR site:zeit.de OR site:dw.com NGLY1"),  # German
    ("zh", "site:news.sina.com.cn OR site:bbc.com/zhongwen OR site:udn.com NGLY1"),  # Chinese
    ("ja", "site:asahi.com OR site:nhk.or.jp OR site:mainichi.jp NGLY1"),  # Japanese
    ("it", "site:corriere.it OR site:repubblica.it OR site:ansa.it NGLY1"),  # Italian
]

GOOGLE_SEARCH_URL = "https://www.google.com/search?q={query}&hl={lang}&gl={country}&num=10"

def fetch_news(query, lang):
    """
    Searches Google for NGLY1 mentions in a specific language.
    """
    search_url = GOOGLE_SEARCH_URL.format(query=query, lang=lang, country="US")
    print(f"Searching: {search_url}")

    response = requests.get(search_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: Unable to fetch results (Status Code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.find_all("div", class_="tF2Cxc"):
        title_tag = result.find("h3")
        link_tag = result.find("a")

        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = link_tag["href"]
            date = datetime.now().strftime("%Y-%m-%d")  # Use current date since Google search doesn't provide timestamps
            results.append({"date": date, "title": title, "url": link, "language": lang})

    return results

def scrape_all():
    """
    Scrapes news articles mentioning NGLY1 in multiple languages.
    """
    all_results = []

    for lang, query in SEARCH_QUERIES:
        try:
            results = fetch_news(query, lang)
            all_results.extend(results)
            time.sleep(random.uniform(2, 5))  # Random delay to avoid Google blocking
        except Exception as e:
            print(f"Error scraping {lang}: {e}")

    return pd.DataFrame(all_results)

def save_to_csv(df, filename="news_mentions.csv"):
    """
    Save the scraped news data to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

def run_cli_mode():
    """
    Run the web scraper in CLI mode.
    """
    df = scrape_all()

    if df.empty:
        print("⚠ No news articles found.")
        return

    save_to_csv(df)
    print(df)

def run_streamlit_mode():
    """
    Run the scraper as a Streamlit web app.
    """
    st.title("NGLY1 Global News Scraper")
    
    df = scrape_all()

    if df.empty:
        st.warning("No articles found.")
        return

    st.success(f"Found {len(df)} relevant articles.")
    st.dataframe(df)

    # Save CSV file
    csv_filename = "news_mentions.csv"
    save_to_csv(df, csv_filename)

    # Provide CSV download link
    with open(csv_filename, "rb") as f:
        st.download_button("Download CSV", f, file_name=csv_filename, mime="text/csv")

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode()
    else:
        run_streamlit_mode()
