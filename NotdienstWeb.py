# pip install python-dotenv
# pip install playwright
# playwright install

import os
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables from .env file
load_dotenv()


def create_html_page_with_logo(pharmacy_list):
    """Creates an HTML page with a logo image in the top left corner.

    Args:
    pharmacy_list (list): A list of dictionaries containing pharmacy details.
    """

    # Get the variables from environment variables
    html_page = os.getenv("HTML-PAGE")
    logo_jpg = os.getenv("LOGO-JPG")
    html_title = os.getenv("HTML-TITLE")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{html_title}</title>
        <meta http-equiv="refresh" content="60">
    </head>
    <body>
        <img src="{logo_jpg}" style="position: absolute; top: 10px; left: 10px;">
        testttt
    </body>
    <script>
        window.addEventListener('load', function() {{
            if ('fullscreen' in document) {{
                document.documentElement.requestFullscreen();
            }} else if ('webkitFullscreen' in document) {{
                document.documentElement.webkitRequestFullscreen();
            }} else if ('mozFullScreen' in document) {{
                document.documentElement.mozRequestFullScreen();
            }} else if ('msFullscreenElement' in document) {{
                document.documentElement.msRequestFullscreen();
            }}
        }});
    </script>
    </html>
    """

    with open(html_page, "w") as f:
        f.write(html_content)

    print(f"HTML page created at: {html_page}")


def sort_pharmacies_by_distance(pharmacy_list):
    """Sorts the pharmacy list by distance in ascending order."""
    return sorted(pharmacy_list, key=lambda x: x["distance"])


def extract_pharmacy_data_from_table(page):
    """Extracts pharmacy data from the table with the ID 'fastSearchResultTable'."""
    pharmacy_list = []

    # Find all rows in the table
    # print(page.content())
    # Find all rows with the class 'searchResultEntry'
    rows = page.query_selector_all(".searchResultEntry")

    print(
        f"Found {len(rows)} pharmacy entries."
    )  # Debug message to check if rows are found

    # Iterate through each row and extract the details
    for index, row in enumerate(rows, start=0):
        name = row.query_selector(".name").inner_text()
        phone = row.query_selector(".phone").inner_text()
        street = row.query_selector(".street").inner_text()
        zip_code = row.query_selector(".zipCode").inner_text()
        location = row.query_selector(".location").inner_text()
        service_time = row.query_selector(".serviceTime").inner_text()
        # distance_text = row.query_selector(
        #     ".distance"
        # ).inner_text()  # Assuming the class for distance is 'distance'
        # Extract the numerical part of the distance and convert it to float
        distance_selector = f"#distance-{index}"
        distance_text = page.query_selector(distance_selector).inner_text()
        print(distance_text)
        distance_value = float(distance_text.replace(" km", "").replace(",", "."))
        print(distance_value)

        # Store the pharmacy data in a list
        pharmacy_data = {
            "name": name,
            "phone": phone,
            "address": f"{street}, {zip_code}, {location}",
            "service_time": service_time,
            "distance": distance_value,
        }

        pharmacy_list.append(pharmacy_data)

    print(pharmacy_list)
    return pharmacy_list


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the location from environment variables
        location = os.getenv("LOCATION")

        # Get the current date in the format dd.MM.yyyy
        current_date = datetime.now().strftime("%d.%m.%Y")

        # Construct the full URL with the dynamic date and location from .env
        full_url = f"https://lak-bayern.notdienst-portal.de/blakportal/?date={current_date}&location={location}"
        print(full_url)
        # Load the webpage
        page.goto(full_url)

        # Wait until the pharmacy entries are loaded
        try:
            page.wait_for_selector(
                ".searchResultEntry", timeout=10000
            )  # Timeout set to 10 seconds for loading the entries
            print("Pharmacy entries found.")  # Debug message for entries found
        except:
            print("Pharmacy entries not found or loading took too long.")
            return

        # Call the function to extract pharmacy data
        pharmacy_list = extract_pharmacy_data_from_table(page)

        # Close the browser
        browser.close()

    # Check if any pharmacies were extracted
    if pharmacy_list:
        print("Extracted pharmacy data (before sorting):")
        for pharmacy in pharmacy_list:
            print(pharmacy)

        # Sort the pharmacy list by distance
        sorted_pharmacy_list = sort_pharmacies_by_distance(pharmacy_list)

        print("\nPharmacy data sorted by distance:")
        for pharmacy in sorted_pharmacy_list:
            print(pharmacy)
    else:
        print("No pharmacy data found.")

    create_html_page_with_logo(sorted_pharmacy_list)


# Run the script
if __name__ == "__main__":
    main()
