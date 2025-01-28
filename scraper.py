import requests
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import streamlit as st

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def fetch_news_from_api(api_key, query, language="en", region="us"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "region": region,
        "apiKey": api_key,
        "sortBy": "publishedAt",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["articles"]
    else:
        st.error(f"Error fetching news: {response.status_code}")
        return []

def analyze_text(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def run_cli_mode(api_key, query):
    articles = fetch_news_from_api(api_key, query)
    print(f"Fetched {len(articles)} articles.")  # Debug: Number of articles
    
    data = []
    for article in articles:
        title = article["title"]
        url = article["url"]
        date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        content = article["content"] or ""  # Handle NoneType content
        entities = analyze_text(content)
        countries = [ent[0] for ent in entities if ent[1] == "GPE"]
        
        print(f"Article: {title}")  # Debug: Article title
        print(f"Detected countries: {countries}")  # Debug: Extracted countries
        
        for country in countries:
            data.append({"date": date, "country": country, "title": title, "url": url})
    
    df = pd.DataFrame(data)
    print("\nDataFrame contents:")  # Debug: Show DataFrame
    print(df)
    
    if df.empty:
        print("No data to plot. Exiting.")
        return
    
    # Plotting code...
    plt.figure(figsize=(10, 6))
    if not df.empty:
        for i, row in df.iterrows():
            plt.scatter(row["date"], row["country"], label=row["title"])
            plt.annotate(
                row["title"],
                (row["date"], row["country"]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center"
            )
        plt.xlabel("Date")
        plt.ylabel("Country")
        plt.title("NGLY1 News Mentions")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("ngly1_news_plot.png")
        print("Plot saved to ngly1_news_plot.png")
    else:
        print("No data to plot.")
        
def run_streamlit_mode():
    # Streamlit mode: Display the app
    st.title("NGLY1 News Mentions")
    api_key = st.text_input("Enter NewsAPI key:", type="password")
    query = st.text_input("Search query:", "NGLY1 deficiency")
    
    if api_key and query:
        articles = fetch_news_from_api(api_key, query)
        if articles:
            st.success(f"Found {len(articles)} articles.")
            data = []
            for article in articles:
                title = article["title"]
                url = article["url"]
                date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                content = article["content"]
                entities = analyze_text(content)
                countries = [ent[0] for ent in entities if ent[1] == "GPE"]
                for country in countries:
                    data.append({"date": date, "country": country, "title": title, "url": url})
            
            df = pd.DataFrame(data)
            st.dataframe(df)
            plt.figure(figsize=(10, 6))
            for i, row in df.iterrows():
                plt.scatter(row["date"], row["country"], label=row["title"])
                plt.annotate(row["title"], (row["date"], row["country"]), textcoords="offset points", xytext=(0, 10), ha="center")
            
            plt.xlabel("Date")
            plt.ylabel("Country")
            plt.title("NGLY1 News Mentions")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt.gcf())
        else:
            st.warning("No articles found.")

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode(api_key="your_api_key", query="NGLY1 deficiency")
    else:
        run_streamlit_mode()
