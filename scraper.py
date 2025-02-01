import requests
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import sys
from collections import Counter
from tabulate import tabulate
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def fetch_news_from_api(api_key, query, language="en", region="us"):
    """
    Fetch news articles from the NewsAPI.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "region": region,
        "apiKey": api_key,
        "sortBy": "publishedAt",
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("articles", [])
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

def analyze_text(text):
    """
    Extract named entities from text.
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def process_articles(articles):
    """
    Extract relevant information from articles and process named entities.
    """
    data = []
    for article in articles:
        title = article.get("title", "No Title")
        url = article.get("url", "#")
        date = article.get("publishedAt")
        content = article.get("content", "")

        if not date:
            continue  # Skip articles without a valid date
        
        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue  # Skip articles with malformed dates

        entities = analyze_text(content)
        locations = [ent[0] for ent in entities if ent[1] == "GPE"]  # Extract locations

        for location in locations:
            data.append({"date": date, "location": location, "title": title, "url": url})

    return pd.DataFrame(data)

def save_to_csv(df, filename="news_mentions.csv"):
    """
    Save the processed data to a CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def run_cli_mode(api_key, query):
    """
    Run the script in CLI mode and save results as CSV.
    """
    articles = fetch_news_from_api(api_key, query)
    df = process_articles(articles)

    if df.empty:
        print("No relevant data found.")
        return

    # Save to CSV
    save_to_csv(df, "news_mentions.csv")

    # Display structured data
    print("\nNews Mentions Data:")
    print(tabulate(df, headers="keys", tablefmt="grid"))

    # Aggregate and count location mentions
    location_counts = Counter(df["location"])
    print("\nTop Locations Mentioned:")
    print(tabulate(location_counts.items(), headers=["Location", "Mentions"], tablefmt="grid"))

    # Plot mentions over time
    plot_data(df)

def plot_data(df):
    """
    Generate and display a scatter plot of mentions over time.
    """
    plt.figure(figsize=(10, 6))
    if not df.empty:
        for _, row in df.iterrows():
            plt.scatter(row["date"], row["location"], label=row["title"])
            plt.annotate(row["title"], (row["date"], row["location"]), textcoords="offset points", xytext=(0, 10), ha="center")

        plt.xlabel("Date")
        plt.ylabel("Location")
        plt.title("NGLY1 News Mentions Over Time")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("ngly1_news_plot.png")
        print("Plot saved as ngly1_news_plot.png")
        plt.show()
    else:
        print("No data available for plotting.")

def run_streamlit_mode():
    """
    Run the script as a Streamlit web app with CSV download option.
    """
    st.title("NGLY1 News Mentions")
    
    api_key = st.text_input("Enter your NewsAPI key:", type="password")
    query = st.text_input("Search Query", "NGLY1 deficiency")
    
    if api_key and query:
        articles = fetch_news_from_api(api_key, query)
        df = process_articles(articles)

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

        # Aggregate location mentions
        location_counts = df["location"].value_counts().reset_index()
        location_counts.columns = ["Location", "Mentions"]
        st.bar_chart(location_counts.set_index("Location"))

        # Display time-series plot
        plt.figure(figsize=(10, 6))
        for _, row in df.iterrows():
            plt.scatter(row["date"], row["location"], label=row["title"])
            plt.annotate(row["title"], (row["date"], row["location"]), textcoords="offset points", xytext=(0, 10), ha="center")
        
        plt.xlabel("Date")
        plt.ylabel("Location")
        plt.title("NGLY1 News Mentions Over Time")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt.gcf())

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode(api_key="your_api_key", query="NGLY1 deficiency")
    else:
        run_streamlit_mode()
