# apt install python3.11-venv
# generate venv pyvenv_wipe
# pip install python-dotenv
# pip install playwright
# playwright install
# playwright install-deps

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables from .env file
load_dotenv()

yesterday_json = ""
today_json = ""


def create_table_elements(local_pharmacy_list):
    max_table_rows = os.getenv("MAX-TABLE-ROWS")
    local_table_html = ""

    for index, pharmacy in enumerate(local_pharmacy_list, start=1):
        if index > int(max_table_rows):
            break
        local_table_html += f"  <tr><td>{pharmacy['name']}</td><td>{pharmacy['address']}</td>\
            <td>{pharmacy['phone']}</td><td>{pharmacy['service_time']}</td>\
            <td>{pharmacy['distance_text']}</td></tr>\n"
    return local_table_html


def create_html_page_with_logo(pharmacy_list):
    """Creates an HTML page with a logo image in the top left corner.

    Args:
    pharmacy_list (list): A list of dictionaries containing pharmacy details.
    """

    # Get the variables from environment variables
    html_page = os.getenv("HTML-PAGE")
    logo_jpg = os.getenv("LOGO-JPG")
    html_title = os.getenv("HTML-TITLE")

    print("Creating HTML page...")
    # Create the HTML table structure
    table_html = "<table>\n"
    table_html += "  <tr><th>Apotheke</th><th>Adresse</th>\
        <th>Telefon</th><th>Zeiten</th><th>Luftlinie</th></tr>\n"

    table_html += create_table_elements(yesterday_json)
    # table_html += "<tr></tr>\n"
    table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    table_html += f"<tr><td>ab</td><td>datum: {datetime.now().strftime('%d.%m.%Y')} 08:30 Uhr</td><td> </td><td> </td><td> </td></tr>\n"
    table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    table_html += create_table_elements(pharmacy_list)

    table_html += "</table>\n"

    # Get the current date and time
    unformatted_datetime = datetime.now()
    # Format the date and time
    formatted_datetime = unformatted_datetime.strftime("%d:%m:%Y %H:%M:%S")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{html_title}</title>
        <meta http-equiv="refresh" content="60">
        <meta charset="utf-8">
        <link rel="stylesheet" href="./styles.css">
    </head>
        <body>
            <p>Aktuelle Uhrzeit: <span id="time-display"></span></p>

            <div style="position: relative;">
                <div style="position: relative; top: 10px; left: 20px;">
                    <h1 style="margin-bottom: 100px;">{html_title}</h1>
                    <img src="Logo_Linden-Apotheke.jpg" style="position: absolute; top: -50px; right: 10px;">
                    {table_html}
                    <br>
                    <p>Generated on { formatted_datetime }</p>

                </div>
            </div>
            <script>
                function updateTime() {{
                    const currentTime = new Date();
                    /*
                    const options = {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' }};
                    */
                    const options = {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }};

                    const timeString = currentTime.toLocaleString('de-DE', options);
                    document.getElementById('time-display').textContent = timeString+ ' Uhr';
                }}

                setInterval(updateTime, 1000); // Update the time every second
            </script>
    </body>
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
    time.sleep(5)

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
            "distance_text": distance_text,
            "distance": distance_value,
        }

        pharmacy_list.append(pharmacy_data)

    print(pharmacy_list)
    return pharmacy_list


def save_json_to_file(json_data, filename):
    """
    Save a JSON string to a file.

    Args:
        json_data (str): The JSON data to be saved.
        filename (str, optional): The name of the file to save the data to. Defaults to "data.json".
    """
    # json_data = '{"name": "John Doe", "age": 35, "email": "john.doe@example.com"}'

    with open(filename, "w") as f:
        json.dump((json_data), f)
        # json.dump(json.loads(json_data), f)
    print(f"JSON data saved to '{filename}' file.")


def load_json_from_file(filename):
    with open(filename, "r") as f:
        data_json = json.load(f)
    print(f"Loaded JSON data from '{filename}' file.")
    print(f"Data: {data_json}")
    return data_json


def check_json_to_file(json_data, filename1="yesterday.json", filename2="today.json"):
    """
    Save a JSON string to a file.

    Args:
        json_data (str): The JSON data to be saved.
        filename (str, optional): The name of the file to save the data to. Defaults to "data.json".
    """

    global yesterday_json
    global today_json

    # save_json_to_file(json_data, filename1)
    # save_json_to_file(json_data, filename2)
    # return

    if yesterday_json == "":
        yesterday_json = load_json_from_file(filename1)

    if today_json == "":
        today_json = load_json_from_file(filename2)

    if json_data != today_json:
        save_json_to_file(today_json, filename1)
        yesterday_json = today_json
        save_json_to_file(json_data, filename2)


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

    check_json_to_file(sorted_pharmacy_list, "yesterday.json", "today.json")
    create_html_page_with_logo(sorted_pharmacy_list)

    # sleep for x minutes
    time.sleep(300)


# Run the script
if __name__ == "__main__":
    # while True:
    main()


# from jinja2 import Template

# # Get the current date and time
# now = datetime.datetime.now()

# # Create a Jinja2 template with a placeholder for the date and time
# template = Template("""
# <!DOCTYPE html>
# <html>
# <head>
# <title>Generated HTML</title>
# </head>
# <body>
# <h1>Generated on {{ now }}</h1>
# </body>
# </html>
# """)
