import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import sys
from collections import Counter
from tabulate import tabulate

# Google News URL (modify for other sources)
GOOGLE_NEWS_URL = "https://news.google.com/search?q=NGLY1+deficiency&hl=en-US&gl=US&ceid=US:en"

def fetch_news():
    """
    Scrape Google News search results for NGLY1 deficiency.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(GOOGLE_NEWS_URL, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    data = []
    for article in articles:
        title_tag = article.find("h3")
        if not title_tag:
            continue
        
        title = title_tag.text.strip()
        link = "https://news.google.com" + title_tag.a["href"][1:] if title_tag.a else "#"
        date = datetime.now().strftime("%Y-%m-%d")  # Use current date as Google News does not provide timestamps

        data.append({"date": date, "title": title, "url": link})

    return pd.DataFrame(data)

def save_to_csv(df, filename="news_mentions.csv"):
    """
    Save the scraped news data to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def plot_data(df):
    """
    Generate and display a scatter plot of news mentions over time.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(df["date"], range(len(df)), label="News Mentions")
    
    plt.xlabel("Date")
    plt.ylabel("Articles")
    plt.title("NGLY1 News Mentions Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ngly1_news_plot.png")
    print("Plot saved as ngly1_news_plot.png")

def run_cli_mode():
    """
    Run the web scraper in CLI mode.
    """
    df = fetch_news()

    if df.empty:
        print("No news articles found.")
        return

    # Save to CSV
    save_to_csv(df, "news_mentions.csv")

    # Display structured data
    print("\nNews Mentions Data:")
    print(tabulate(df, headers="keys", tablefmt="grid"))

    # Plot mentions over time
    plot_data(df)

def run_streamlit_mode():
    """
    Run the web scraper as a Streamlit web app.
    """
    st.title("NGLY1 News Scraper")

    # Fetch news
    df = fetch_news()

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

    # Display scatter plot
    plot_data(df)
    st.image("ngly1_news_plot.png", caption="News Mentions Over Time")

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode()
    else:
        run_streamlit_mode()
