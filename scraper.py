import requests
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Fetch news from NewsAPI
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

# Analyze text with spaCy
def analyze_text(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Main function
def main():
    st.title("NGLY1 News Mentions")

    # Input fields for API key and query
    api_key = st.text_input("Enter your NewsAPI key:", type="password")
    query = st.text_input("Enter search query:", "NGLY1 deficiency")

    if api_key and query:
        st.write("Fetching news articles...")
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
                countries = [ent[0] for ent in entities if ent[1] == "GPE"]  # Extract countries
                for country in countries:
                    data.append({"date": date, "country": country, "title": title, "url": url})

            df = pd.DataFrame(data)

            # Display the data as a table
            st.write("### Extracted Data")
            st.dataframe(df)

            # Plot
            st.write("### NGLY1 News Mentions Over Time")
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

            # Display the plot in Streamlit
            st.pyplot(plt.gcf())

        else:
            st.warning("No articles found.")
    else:
        st.warning("Please enter your NewsAPI key and search query.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
