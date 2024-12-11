import os
import requests
# import xml.etree.ElementTree as ET
from lxml import etree


class ImportApiData:
    """
    A class used to import pharmacy data from an XML API.
    """

    def __init__(self, api_url):
        """
        Initializes the ImportApiData object with an API URL.

        Args:
            api_url (str): The URL of the XML API.
        """
        self.api_url = api_url

    def import_data(self):
        """
        Imports data from the XML API.

        Returns:
            list: A list of dictionaries containing pharmacy data.
        """
        xml_file=os.getenv('XML_FILE')

        if os.getenv('TEST_MODE') == 'True':
            test_xml_file = os.getenv('TEST_XML_FILE')
            xml_root = etree.parse(source=test_xml_file).getroot() # type: ignore
        else:
            response = requests.get(self.api_url)
            if response.status_code != 200:
                print(f"Failed to retrieve data from API. Status code: {response.status_code}")
                return []
            xml_data = response.content
            xml_root = etree.fromstring(xml_data) # type: ignore
        try:
            with open(xml_file, "wb") as f: # type: ignore
                f.write(etree.tostring(xml_root, pretty_print=True, encoding='utf-8')) # type: ignore
                print(f"XML saved to {xml_file}")
        except IOError as e:
            print(f"An error occurred while saving XML data to {xml_file}: {e}") # type: ignore


        print(etree.tostring(xml_root, pretty_print=True).decode()) # type: ignore

        pharmacy_list = []

        for entry_element in xml_root.findall(".//entries/entry"):
            pharmacy_data = {
                "id": entry_element.find("id").text,
                "from": entry_element.find("from").text,
                "to": entry_element.find("to").text,
                "name": entry_element.find("name").text,
                "street": entry_element.find("street").text,
                "zipCode": entry_element.find("zipCode").text,
                "location": entry_element.find("location").text,
                "subLocation": entry_element.find("subLocation").text,
                "phone": entry_element.find("phone").text,
                "lat": float(entry_element.find("lat").text),
                "lon": float(entry_element.find("lon").text),
            }

            pharmacy_list.append(pharmacy_data)

        return pharmacy_list

    # def save_xml_to_file(self, xml_data, filename):
    #     """
    #     Save XML data to a file.

    #     Args:
    #         xml_data (str): The XML data to be saved.
    #         filename (str, optional): The name of the file to save the data to. Defaults to "data.xml".
    #     """

    #     with open(filename, "w", encoding="utf-8") as f:
    #         f.write(xml_data.decode())
    #     print(f"XML data saved to '{filename}' file.")

