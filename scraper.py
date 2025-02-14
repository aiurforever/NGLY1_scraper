import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

# Define the keyword to search for
keyword = "NGLY1"

# Curated dictionary of 20 medical websites, grouped by region.
# Replace these URLs if needed with the most current sites.
medical_publication_websites = {
    "US": [
        "https://www.medicalnewstoday.com/",                   # Medical News Today
        "https://www.medscape.com/",                             # Medscape
        "https://www.healthline.com/health-news?ref=global",      # Healthline
        "https://www.nytimes.com/section/health",                # NYT Health
        "https://www.statnews.com/"                              # STAT News
    ],
    "UK/Europe": [
        "https://www.sciencemediacentre.org/",                   # Science Media Centre
        "https://www.sciencedaily.com/news/top/health/",         # ScienceDaily – Health News
        "https://www.who.int/",                                  # WHO
        "https://www.nhs.uk/",                                   # NHS
        "https://www.healtheuropa.eu/",                          # Healtheuropa
        "https://www.theconversation.com/",                      # The Conversation
        "https://www.bbc.com/news/health",                       # BBC News – Health
        "https://www.cochranelibrary.com/",                      # Cochrane Library
        "https://www.news-medical.net/"                          # News Medical
    ],
    "New Zealand": [
        "https://www.health.govt.nz/"                            # Ministry of Health New Zealand
    ],
    "Japan": [
        "https://www.m3.com/",                                   # M3.com
        "https://www.jmaj.jp/",                                  # JMA Journal
        "https://www3.nhk.or.jp/nhkworld/en/section/health/"      # NHK World – Health
    ],
    "China": [
        "https://www.dxy.cn/",                                   # DXY.cn
        "https://www.haodf.com/"                                 # HaoDF (Good Doctor)
    ]
}

results = []

def get_full_url(base, link):
    """Convert relative URLs to absolute URLs."""
    return urllib.parse.urljoin(base, link)

# Iterate over each region and its list of websites
for region, websites in medical_publication_websites.items():
    for site in websites:
        try:
            print(f"Scraping {site} ({region})...")
            # Fetch the page content using a browser-like user-agent
            response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                print(f"Could not retrieve {site} (Status code: {response.status_code})")
                continue
            
            # Ensure proper encoding is used
            if response.encoding is None:
                response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all anchor tags with href attributes
            anchors = soup.find_all('a', href=True)
            for anchor in anchors:
                link_text = anchor.get_text().strip()
                href = anchor['href']
                full_url = get_full_url(site, href)
                
                # Check if the keyword appears in the visible text or the URL (case-insensitive)
                if keyword.lower() in link_text.lower() or keyword.lower() in full_url.lower():
                    results.append({
                        'region': region,
                        'source_website': site,
                        'link_text': link_text,
                        'link': full_url
                    })
        except Exception as e:
            print(f"Error scraping {site}: {e}")

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Save the DataFrame to an Excel file
output_filename = "ngly1_medical_publications_links.xlsx"
df.to_excel(output_filename, index=False)
print(f"Results saved to {output_filename}")
