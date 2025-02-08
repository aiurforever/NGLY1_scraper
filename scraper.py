import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

# Define the keyword to search for
keyword = "NGLY1"

# Curated dictionary of medical publication websites by region.
# Note: The URLs below are examples and may need to be updated with the correct top sites.
medical_publication_websites = {
    "US": [
        "https://www.nejm.org",          # New England Journal of Medicine
        "https://jamanetwork.com",       # JAMA Network
        "https://www.medscape.com"        # Medscape
    ],
    "China": [
        "http://www.cmj.org",            # Chinese Medical Journal (example)
        "http://www.chinajournalofinternalmedicine.com",  # Placeholder for another Chinese medical publication
        "http://www.chinamedicine.org"    # Placeholder
    ],
    "Japan": [
        "https://www.jmaj.jp",           # Japanese Medical Association Journal (example)
        "https://www.jstage.jst.go.jp",    # J-STAGE (platform for Japanese journals)
        "https://www.medicaljournal.jp"    # Placeholder for a Japanese medical publication site
    ],
    "Europe": [
        "https://www.bmj.com",           # British Medical Journal (UK)
        "https://www.thelancet.com",       # The Lancet (UK)
        "https://www.ejin.org"           # Example: European Journal of Internal Medicine (placeholder)
    ],
    "Turkey": [
        "https://www.tmmdergisi.org",     # Example Turkish Medical Journal
        "https://www.turkishmedicaljournal.com",  # Placeholder
        "https://www.journalofturkishmedicine.org" # Placeholder
    ],
    "Korea": [
        "https://www.kjms.org",          # Korean Journal of Medical Science
        "https://www.jkma.org",           # Journal of the Korean Medical Association
        "https://www.kiom.org"            # Placeholder for another Korean medical site
    ],
    "Latin America": [
        "https://www.scielo.org",         # SciELO (Scientific Electronic Library Online; collection for Latin America)
        "https://www.revistas.usp.br",    # Journals from the University of São Paulo
        "https://www.medicaljournalla.com" # Placeholder for a Latin American medical publication
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
