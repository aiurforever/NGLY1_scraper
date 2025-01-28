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
    # ... (same as before) ...

def analyze_text(text):
    # ... (same as before) ...

def run_cli_mode(api_key, query):
    # CLI mode: Run scraping/analysis without Streamlit
    articles = fetch_news_from_api(api_key, query)
    data = []
    for article in articles:
        # ... (same as before) ...
    df = pd.DataFrame(data)
    
    # Save the plot as an image
    plt.figure(figsize=(10, 6))
    # ... (plotting logic) ...
    plt.savefig("ngly1_news_plot.png")
    print("Plot saved to ngly1_news_plot.png")

def run_streamlit_mode():
    # Streamlit mode: Display the app
    st.title("NGLY1 News Mentions")
    api_key = st.text_input("Enter NewsAPI key:", type="password")
    query = st.text_input("Search query:", "NGLY1 deficiency")
    
    if api_key and query:
        articles = fetch_news_from_api(api_key, query)
        # ... (display data/plot) ...

if __name__ == "__main__":
    if "--cli" in sys.argv:
        # Run in CLI mode (for GitHub Actions)
        run_cli_mode(api_key="your_api_key", query="NGLY1 deficiency")
    else:
        # Run in Streamlit mode (for local/dev)
        run_streamlit_mode()
