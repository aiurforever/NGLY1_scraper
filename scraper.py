import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

# Define the keyword to search for
keyword = "NGLY1"

# Curated dictionary of medical publication websites by region.
# NOTE: The URLs below are examples and placeholders. Replace these with the actual top 20 medical websites for each region.
medical_publication_websites = {
    "US": [
        "https://www.nejm.org",                # New England Journal of Medicine
        "https://jamanetwork.com",             # JAMA Network
        "https://www.medscape.com",             # Medscape
        "https://www.lancet.com",               # The Lancet (US version/affiliate if available)
        "https://www.bmj.com",                  # BMJ (even though UK-based, often cited in US research)
        "https://www.acpjournals.org",          # ACP Journals
        "https://www.aappublications.org",      # AAP Publications
        "https://www.ahajournals.org",          # American Heart Association Journals
        "https://www.cmaj.ca",                  # Canadian Medical Association Journal (often read in the US)
        "https://www.plos.org",                 # PLOS (Public Library of Science)
        "https://www.nature.com/medicine",      # Nature Medicine
        "https://www.sciencemag.org",           # Science (medicine-related articles)
        "https://www.cell.com",                 # Cell (for biomedical research)
        "https://www.nejm.org",                 # Duplicate intentional for illustration (update/remove as needed)
        "https://www.medicalnewstoday.com",     # Medical News Today
        "https://www.webmd.com",                # WebMD (health information)
        "https://www.mayoclinic.org",           # Mayo Clinic
        "https://www.uptodate.com",             # UpToDate (clinical information)
        "https://www.medpagetoday.com",         # MedPage Today
        "https://www.medicaldaily.com"          # Medical Daily
    ],
    "China": [
        "http://www.cmj.org",                                # Chinese Medical Journal
        "http://www.chinajournalofinternalmedicine.com",     # Placeholder
        "http://www.chinamedicine.org",                      # Placeholder
        "http://www.cma.org.cn",                             # Chinese Medical Association (placeholder)
        "http://www.chinajournal.net",                       # Placeholder
        "http://www.medscimonit.com",                        # Medical Science Monitor (if available in Chinese)
        "http://www.chinajournalofclinicalpharmacology.com", # Placeholder
        "http://www.chinajournalofneurology.com",            # Placeholder
        "http://www.chinajournalofcardiology.com",           # Placeholder
        "http://www.chinajournalofsurgery.com",              # Placeholder
        "http://www.chinajournalofpediatrics.com",           # Placeholder
        "http://www.chinajournalofdermatology.com",          # Placeholder
        "http://www.chinajournalofendocrinology.com",        # Placeholder
        "http://www.chinajournalofobstetrics.com",           # Placeholder
        "http://www.chinajournalofoncology.com",            # Placeholder
        "http://www.chinajournalofradiology.com",           # Placeholder
        "http://www.chinajournalofpathology.com",           # Placeholder
        "http://www.chinajournalofimmunology.com",          # Placeholder
        "http://www.chinajournalofpharmacology.com",        # Placeholder
        "http://www.chinajournalofepidemiology.com"         # Placeholder
    ],
    "Japan": [
        "https://www.jmaj.jp",              # Japanese Medical Association Journal
        "https://www.jstage.jst.go.jp",       # J-STAGE (platform for Japanese journals)
        "https://www.medicaljournal.jp",      # Placeholder for a Japanese medical publication site
        "https://www.jpnmedassoc.org",        # Japanese Medical Association (placeholder)
        "https://www.journalofjapanesemedicine.jp",  # Placeholder
        "https://www.japansurgery.org",       # Placeholder
        "https://www.japanpediatrics.org",    # Placeholder
        "https://www.japancardiology.jp",     # Placeholder
        "https://www.japancancer.org",        # Placeholder
        "https://www.japanneurology.jp",      # Placeholder
        "https://www.japandermatology.jp",      # Placeholder
        "https://www.japanendocrinology.jp",    # Placeholder
        "https://www.japanobstetrics.org",      # Placeholder
        "https://www.japanorthopedics.jp",      # Placeholder
        "https://www.japansurgeryjournal.jp",   # Placeholder
        "https://www.japanclinicalres.org",     # Placeholder
        "https://www.japanpharmacology.jp",     # Placeholder
        "https://www.japanscienceofmedicine.jp",# Placeholder
        "https://www.japanimmunology.jp",       # Placeholder
        "https://www.japanradiology.jp"         # Placeholder
    ],
    "Europe": [
        "https://www.bmj.com",              # British Medical Journal
        "https://www.thelancet.com",          # The Lancet
        "https://www.ejin.org",              # European Journal of Internal Medicine (placeholder)
        "https://www.europeanheartjournal.com",  # Placeholder for European journals
        "https://www.europeanjournalofmedicine.com", # Placeholder
        "https://www.europeanchildrensjournal.com",   # Placeholder
        "https://www.europeanneurology.com",          # Placeholder
        "https://www.europeancancerjournal.com",      # Placeholder
        "https://www.europeanendocrinology.com",       # Placeholder
        "https://www.europeansurgery.com",            # Placeholder
        "https://www.europeanpsychiatry.com",           # Placeholder
        "https://www.europeaninfectiousdiseases.com",   # Placeholder
        "https://www.europeanobstetrics.com",           # Placeholder
        "https://www.europeancardiology.com",           # Placeholder
        "https://www.europeandermatology.com",          # Placeholder
        "https://www.europeanimmunology.com",           # Placeholder
        "https://www.europeanhematology.com",          # Placeholder
        "https://www.europeanpharmacology.com",         # Placeholder
        "https://www.europeanradiology.com",            # Placeholder
        "https://www.europeanpathology.com"             # Placeholder
    ],
    "Turkey": [
        "https://www.tmmdergisi.org",         # Example Turkish Medical Journal
        "https://www.turkishmedicaljournal.com",  # Placeholder
        "https://www.journalofturkishmedicine.org", # Placeholder
        "https://www.turkishjournals.com",      # Placeholder
        "https://www.medicaljournalturkey.com", # Placeholder
        "https://www.turkeymedicalnews.com",    # Placeholder
        "https://www.turkeyhealthjournal.com",  # Placeholder
        "https://www.ankaramedicaljournal.com", # Placeholder
        "https://www.istanbulmedicaljournal.com",# Placeholder
        "https://www.turkeycardiology.com",     # Placeholder
        "https://www.turkeyneurology.com",      # Placeholder
        "https://www.turkeyoncology.com",       # Placeholder
        "https://www.turkeypediatrics.com",     # Placeholder
        "https://www.turkeydermatology.com",    # Placeholder
        "https://www.turkeyendocrinology.com",  # Placeholder
        "https://www.turkeyimmunology.com",     # Placeholder
        "https://www.turkeysurgery.com",        # Placeholder
        "https://www.turkeyradiology.com",      # Placeholder
        "https://www.turkeypathology.com",      # Placeholder
        "https://www.turkeyinfectiousdiseases.com" # Placeholder
    ],
    "Korea": [
        "https://www.kjms.org",             # Korean Journal of Medical Science
        "https://www.jkma.org",              # Journal of the Korean Medical Association
        "https://www.kiom.org",              # Placeholder for another Korean medical site
        "https://www.koreamed.org",          # Placeholder
        "https://www.koreamedicine.com",     # Placeholder
        "https://www.koreanhealthjournal.com", # Placeholder
        "https://www.koreancardiology.com",   # Placeholder
        "https://www.koreanneurology.com",      # Placeholder
        "https://www.koreansurgery.com",       # Placeholder
        "https://www.koreapediatrics.com",     # Placeholder
        "https://www.koreancancerjournal.com", # Placeholder
        "https://www.koreanendocrinology.com",  # Placeholder
        "https://www.koreandermatology.com",     # Placeholder
        "https://www.koreanimmunology.com",      # Placeholder
        "https://www.koreanpathology.com",       # Placeholder
        "https://www.koreaninfectiousdiseases.com", # Placeholder
        "https://www.koreanpharmacology.com",    # Placeholder
        "https://www.koreanradiology.com",       # Placeholder
        "https://www.koreanobstetrics.com",        # Placeholder
        "https://www.koreanpsychiatry.com"         # Placeholder
    ],
    "Latin America": [
        "https://www.scielo.org",            # SciELO
        "https://www.revistas.usp.br",       # Journals from the University of São Paulo
        "https://www.medicaljournalla.com",  # Placeholder for a Latin American medical publication
        "https://www.latinamericamedicine.com",  # Placeholder
        "https://www.latinamericajournalofmedicine.com", # Placeholder
        "https://www.latinamericaclinicaljournal.com",   # Placeholder
        "https://www.latinamericaneurology.com",         # Placeholder
        "https://www.latinamericacardiology.com",        # Placeholder
        "https://www.latinamericacancerjournal.com",     # Placeholder
        "https://www.latinamericapharmacology.com",      # Placeholder
        "https://www.latinamericadiagnosticjournal.com", # Placeholder
        "https://www.latinamericahospitalmedicine.com",  # Placeholder
        "https://www.latinamericasurgery.com",           # Placeholder
        "https://www.latinamericapediatrics.com",        # Placeholder
        "https://www.latinamericadermatology.com",       # Placeholder
        "https://www.latinamericaendocrinology.com",     # Placeholder
        "https://www.latinamericainfectiousdiseases.com",  # Placeholder
        "https://www.latinamericadiagnosticimaging.com",   # Placeholder
        "https://www.latinamericatherapy.com",           # Placeholder
        "https://www.latinamericajournalofhealth.com"    # Placeholder
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
