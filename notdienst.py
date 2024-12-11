"""
Pharmacy Scraper: A Python script that scrapes pharmacy data from a webpage,
sorts the data by distance, and generates an HTML page with the sorted data.

Dependencies:
- Python 3.11
- pip
- python-dotenv
- playwright
- Jinja2 (for HTML templating)

Functionality:
1. Load environment variables from a .env file.
2. Launch a headless browser using Playwright.
3. Navigate to the specified webpage and extract pharmacy data from a table.
4. Sort the extracted data by distance.
5. Generate an HTML page using Jinja2 template with the sorted data.
6. Save the HTML page to a specified file.
7. Sleep for a specified duration before repeating the process.
"""

# The rest of the Python script follows...# apt install python3.11-venv
# generate venv pyvenv_wipe
# pip install python-dotenv
# pip install playwright
# playwright install
# playwright install-deps

import html
import os
import json
import time
import datetime

# import jinja2
from datetime import datetime
from dotenv import load_dotenv
# from playwright.sync_api import sync_playwright
# from scraper import Scraper
from importapidata import ImportApiData

from htmlcreator import HtmlCreator
# Load environment variables from .env file
load_dotenv()

yesterday_json_data = ""
today_json_data = ""



def main():

    # Load environment variables from .env file
    html_page = os.getenv("HTML_PAGE")
    html_title = os.getenv("HTML_TITLE")
    html_logo = os.getenv("HTML_LOGO")
    html_template = os.getenv("HTML_TEMPLATE")

    # scraper = Scraper("https://example.com/pharmacies")
    # scraper.load_page()
    # pharmacy_list = scraper.scrape_pharmacy_data()

    api_url = os.getenv("API_URL")
    importer = ImportApiData(api_url)
    pharmacy_list = importer.import_data()
    print(pharmacy_list)
    # importer.save_xml_to_file(pharmacy_list, os.getenv("JSON_FILE"))

    # Check if any pharmacies were extracted
    if pharmacy_list:
        print("Extracted pharmacy data (before sorting):")
        for pharmacy in pharmacy_list:
            print(pharmacy)

        # Sort the pharmacy list by distance
        # sorted_pharmacy_list = sort_pharmacies_by_distance(pharmacy_list)

        # print("\nPharmacy data sorted by distance:")
        # for pharmacy in sorted_pharmacy_list:
        #     print(pharmacy)
    else:
        print("No pharmacy data found.")

    # Create an HTML page using Jinja2 template
    html_creator = HtmlCreator(html_page, html_title, html_logo, html_template)
    # Create the content, of the html page
    for pharmacy in pharmacy_list:
        from_date = datetime.strptime(pharmacy["from"], "%Y-%m-%dT%H:%M:%S.%f+00:00")
        to_date = datetime.strptime(pharmacy["to"], "%Y-%m-%dT%H:%M:%S.%f+00:00")
        
        pharmacy["from"] = from_date.strftime("%d.%m.%y %H:%M")
        pharmacy["to"] = to_date.strftime("%d.%m.%y %H:%M")
    html_page_detail_content = html_creator.create_html(pharmacy_list)

    # Save the HTML page content to the specified file
    html_creator.save_html_to_file(html_page_detail_content)

# Run the script
if __name__ == "__main__":
    # while True:
    main()
