import os
import requests
import spacy
import pandas as pd
import sys
from datetime import datetime

# Load spaCy model (handle missing model error)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model missing! Run: python -m spacy download en_core_web_sm")
    sys.exit(1)

def fetch_news_from_api():
    """
    Fetch news articles using NewsAPI.
    """
    api_key = os.getenv("NEWSAPI_KEY")  # Read API key from environment variable

    if not api_key:
        print("ERROR: NEWSAPI_KEY is missing! Set it in GitHub Secrets.")
        sys.exit(1)  # Exit with error

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "NGLY1 deficiency",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        sys.exit(1)

def process_articles(articles):
    """
    Extract relevant information from articles.
    """
    data = []
    for article in articles:
        title = article.get("title", "No Title")
        url = article.get("url", "#")
        date = article.get("publishedAt", datetime.utcnow().isoformat())

        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue

        data.append({"date": date, "title": title, "url": url})

    return pd.DataFrame(data)

def run_cli_mode():
    """
    Run the script in CLI mode.
    """
    try:
        articles = fetch_news_from_api()
        df = process_articles(articles)

        if df.empty:
            print("No relevant data found.")
            sys.exit(1)

        df.to_csv("news_mentions.csv", index=False)
        print("Data saved to news_mentions.csv")

    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode()
