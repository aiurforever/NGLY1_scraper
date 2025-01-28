import requests
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
        print(f"Error fetching news: {response.status_code}")
        return []

# Analyze text with spaCy
def analyze_text(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Main function
def main():
    api_key = "your_newsapi_key"
    query = "NGLY1 deficiency"
    articles = fetch_news_from_api(api_key, query)

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

    # Plot
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
    plt.savefig("ngly1_news_plot.png")  # Save the plot as an image
    plt.show()

if __name__ == "__main__":
    main()
