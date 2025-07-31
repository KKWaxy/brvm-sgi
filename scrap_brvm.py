import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

brvm_sg_url = "https://www.brvm.org/fr/intervenants/sgi/tous"

# scrap_brvm.py
# This script scrapes the BRVM (Bourse Régionale des Valeurs Mobilières) website
# to collect information about SGI (Sociétés de Gestion et d'Intermédiation).
# It retrieves details such as name, address, BP (Boîte Postale), email, fax, telephone, and website.

BRVM_SGI = []
PAGES = 10
def pasrse_html(html_content):
    for row in html_content.find_all('div', class_='views-row'):
        data = row.find( attrs={"class": "views-field-nothing"})
        if not data:
            continue
        else:
            nom = data.find('img').next_sibling
            if nom:
                nom = str(nom).strip()
            else:
                nom = "N/A"
            address = data.find('div', class_='adresse_sgi')
            if address:
                address = address.get_text(strip=True)
            else:
                address = "N/A"
            bp = data.find('div', class_='bp')
            if bp:
                bp = bp.get_text(strip=True)
            else:
                bp = "N/A"
            email = data.find('div', class_=re.compile(r"email_sgi"))
            if email:
                email = email.get_text(strip=True)
            else:
                email = "N/A"
            fax = data.find('div', class_='fax_sgi')
            if fax:
                fax = fax.get_text(strip=True)
            else:
                fax = "N/A"
            telephone = data.find('div', class_='tel_sgi')
            if telephone:
                telephone = telephone.get_text(strip=True)
            else:
                telephone = "N/A"
            site_web = data.find('div', class_='site_sgi')
            if site_web:
                site_web = site_web.get_text(strip=True)
            else:
                site_web = "N/A"

            BRVM_SGI.append({
                "Nom": nom,
                "Adresse": address,
                "BP": bp,
                "Email":email,                
                "Fax": fax,
                "Téléphone": telephone,
                "Site Web": site_web,
            })
    
def get_raw_data(page=None):
    """
    Fetches the raw HTML content from the given URL.
    """
    url = brvm_sg_url
    global PAGES 
    if page:
        url = f"{url}?page={page}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        parse_html = BeautifulSoup(response.content, 'html.parser').css.select_one('div.view-content')
        pasrse_html(parse_html)
    else:
        pass
    PAGES -= 1
    page = PAGES
    if page in range(1, 11):
        print(f"Scraping page {page}...")
        get_raw_data(page)

if __name__ == "__main__":
    """
    Main function to execute the scraping and save the data to a CSV file.
    """
    print("Starting to scrape BRVM SGI data...")
    get_raw_data()
    df = pd.DataFrame(BRVM_SGI)
    df.to_csv('brvm_sgi.csv', index=False, encoding='utf-8-sig')
    print("Data scraped and saved to brvm_sgi.csv") 