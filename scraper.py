import requests
from bs4 import BeautifulSoup
from googlesearch import search
from langdetect import detect

# Define keywords and languages
keywords = ["NGLY1 deficiency", "NGLY1 patients", "NGLY1 mutation"]
languages = ["en", "es", "fr", "de"]  # English, Spanish, French, German
regions = ["us", "uk", "es", "fr", "de"]  # USA, UK, Spain, France, Germany

# Function to scrape content from a URL
def scrape_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract text from the page
        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to search for mentions of NGLY1
def search_ngly1_mentions(keyword, lang, region, num_results=10):
    query = f"{keyword} site:.{region}"
    results = []
    try:
        for url in search(query, num=num_results, stop=num_results, pause=2, lang=lang):
            print(f"Found URL: {url}")
            content = scrape_url(url)
            if content and keyword.lower() in content.lower():
                results.append({"url": url, "content": content})
    except Exception as e:
        print(f"Error searching for {keyword} in {lang}: {e}")
    return results

# Main function to search across languages and regions
def main():
    all_results = []
    for keyword in keywords:
        for lang in languages:
            for region in regions:
                print(f"Searching for '{keyword}' in {lang} (region: {region})...")
                results = search_ngly1_mentions(keyword, lang, region)
                all_results.extend(results)
    
    # Save results to a file
    with open("ngly1_mentions.txt", "w", encoding="utf-8") as f:
        for result in all_results:
            f.write(f"URL: {result['url']}\n")
            f.write(f"Content: {result['content'][:500]}...\n\n")  # Save first 500 chars

    print(f"Found {len(all_results)} mentions of NGLY1.")

if __name__ == "__main__":
    main()
