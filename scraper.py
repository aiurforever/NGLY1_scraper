import requests
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import sys
from collections import Counter
from tabulate import tabulate

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

def plot_dat
