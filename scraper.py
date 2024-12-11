# scraper.py

class Scraper:
    """
    A class used to scrape pharmacy data from a webpage.
    """

    def __init__(self, url):
        """
        Initializes the Scraper object with a URL.

        Args:
            url (str): The URL of the webpage to scrape.
        """
        self.url = url
        self.page = None  # The Playwright page object

    def load_page(self):
        """
        Loads the webpage and waits for the pharmacy entries to be loaded.

        Returns:
            None
        """
        with sync_playwright() as p:
            # Launch a new browser instance in headless mode
            browser = p.chromium.launch(headless=True)
            # Create a new page object
            self.page = browser.new_page()
            # Navigate to the specified URL
            self.page.goto(self.url)

            try:
                # Wait for the pharmacy entries to be loaded
                self.page.wait_for_selector(".searchResultEntry", timeout=10000)
                print("Pharmacy entries found.")
            except TimeoutError:
                # Handle timeout error
                print(f"Loading the {self.url} took too long. ")
                return
            except Exception as e:
                # Handle any other exceptions
                print(f"An unexpected error occurred: {e}")
                return

    def scrape_pharmacy_data(self):
        """
        Scrapes the pharmacy data from the loaded webpage.

        Returns:
            list: A list of dictionaries containing pharmacy data.
        """
        if not self.page:
            # Check if the page has been loaded
            print("Please load the page first using the load_page method.")
            return

        pharmacy_list = []  # Initialize an empty list to store pharmacy data

        # Get all pharmacy entry elements
        rows = self.page.query_selector_all(".searchResultEntry")

        print(f"Found {len(rows)} pharmacy entries.")

        for index, row in enumerate(rows, start=0):
            # Extract data from each pharmacy entry element
            name = row.query_selector(".name").inner_text()
            phone = row.query_selector(".phone").inner_text()
            street = row.query_selector(".street").inner_text()
            zip_code = row.query_selector(".zipCode").inner_text()
            location = row.query_selector(".location").inner_text()
            service_time = row.query_selector(".serviceTime").inner_text()
            distance_selector = f"#distance-{index}"
            distance_text = self.page.query_selector(distance_selector).inner_text()
            distance_value = float(distance_text.replace(" km", "").replace(",", "."))

            # Create a dictionary to store pharmacy data
            pharmacy_data = {
                "name": name,
                "phone": phone,
                "address": f"{street}, {zip_code}, {location}",
                "service_time": service_time,
                "distance_text": distance_text,
                "distance": distance_value,
            }

            # Add pharmacy data to the list
            pharmacy_list.append(pharmacy_data)

        print(pharmacy_list)
        return pharmacy_list
    


    
# MY STUFF
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=True)
    #     page = browser.new_page()

    #     # Get the location from environment variables
    #     location = os.getenv("LOCATION")

    #     # Get the current date in the format dd.MM.yyyy
    #     current_date = datetime.now().strftime("%d.%m.%Y")

    #     start_url = "https://lak-bayern.notdienst-portal.de/blakportal"
    #     # Construct the full URL with the dynamic date and location from .env
    #     full_url = f"{start_url}/?date={current_date}&location={location}"
    #     print(full_url)

    #     # Load the webpage
    #     page.goto(full_url)

    #     # Wait until the pharmacy entries are loaded
    #     try:
    #         page.wait_for_selector(
    #             ".searchResultEntry", timeout=10000
    #         )  # Timeout set to 10 seconds for loading the entries
    #         print("Pharmacy entries found.")  # Debug message for entries found
    #     except TimeoutError:
    #         print(f"Loading the {full_url} took too long. ")
    #         return
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    #         return

    #     # Call the function to extract pharmacy data
    #     pharmacy_list = extract_pharmacy_data_from_table(page)

    #     # Close the browser
    #     browser.close()
