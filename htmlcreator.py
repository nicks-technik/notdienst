import os
import html
from datetime import datetime
from jinja2 import Template

class HtmlCreator:
    """A class used to create an HTML page with a logo image in the top left corner.
    """

    def __init__(self, html_page, html_title, html_logo_left, html_logo_right, html_template):
        """
        Initializes the HtmlCreator object with the necessary parameters.

        Parameters:
            html_page (str): The path to the HTML page.
            html_title (str): The title of the HTML page.
            html_logo (str): The path to the logo image.
        """
        self.html_page = html_page
        self.html_title = html_title
        self.html_logo_left = html_logo_left
        self.html_logo_right = html_logo_right
        self.html_template = html_template


    def create_html(self, local_pharmacy_list):
        """
        Creates an HTML page from a template and a list of local pharmacies.

        Parameters:
            local_pharmacy_list (list): A list of dictionaries containing pharmacy information.
                Each dictionary should have the following keys:
                    - name: The name of the pharmacy.
                    - address: The address of the pharmacy.
                    - phone: The phone number of the pharmacy.
                    - service_time: The service time of the pharmacy.
                    - distance_text: The distance to the pharmacy.

        Returns:
            str: The rendered HTML page as a string.
        """
        # Load the Jinja2 template
        template = Template(open(self.html_template, 'r').read())
        # Extract the data from the XML
        data = {
            'local_pharmacy_list': local_pharmacy_list,
            'html_logo_left': self.html_logo_left,
            'html_logo_right': self.html_logo_right,
            'html_title': self.html_title,
            'generated_at': datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        }
        # Render the template with the data
        html_page_content = template.render(**data)
        # Print the rendered HTML
        print(html_page_content)
        return html_page_content

    def save_html_to_file(self, html_content):
#         """Saves the HTML content to a file.

#         Args:
#         html_content (str): The HTML content to be saved.
#         """
        with open(self.html_page, 'w', encoding='utf-8') as f:
            f.write(html_content)
            print(f"HTML page saved to {self.html_page}")


    # def create_table_elements(self, local_pharmacy_list):
    #     """
    #     Creates an HTML table from a list of local pharmacies.

    #     Parameters:
    #         local_pharmacy_list (list): A list of dictionaries containing pharmacy information.
    #             Each dictionary should have the following keys:
    #                 - name: The name of the pharmacy.
    #                 - address: The address of the pharmacy.
    #                 - phone: The phone number of the pharmacy.
    #                 - service_time: The service time of the pharmacy.
    #                 - distance_text: The distance to the pharmacy.

    #     Returns:
    #         str: The HTML table as a string.
    #     """
    #     max_table_rows = os.getenv("MAX-TABLE-ROWS")
    #     local_table_html = ""

    #     for index, pharmacy in enumerate(local_pharmacy_list, start=1):
    #         if index > int(max_table_rows):
    #             break
    #         local_table_html += f"  <tr><td>{pharmacy['name']}</td><td>{pharmacy['address']}</td>\
    #             <td>{pharmacy['phone']}</td><td>{pharmacy['service_time']}</td>\
    #             <td>{pharmacy['distance_text']}</td></tr>\n"
    #     return local_table_html

    # def create_html_page_with_logo(self, pharmacy_list):
    #     """Creates an HTML page with a logo image in the top left corner.

    #     Args:
    #     pharmacy_list (list): A list of dictionaries containing pharmacy details.
    #     """

    #     # Create the HTML table structure
    #     table_html = "<table>\n"
    #     table_html += "  <tr><th>Apotheke</th><th>Adresse</th>\
    #         <th>Telefon</th><th>Zeiten</th><th>Luftlinie</th></tr>\n"

    #     table_html += self.create_table_elements(yesterday_json_data)
    #     # table_html += "<tr></tr>\n"
    #     table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    #     table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    #     table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    #     table_html += f"<tr><td>ab</td><td>datum: {datetime.now().strftime('%d.%m.%Y')} 08:30 Uhr</td>\
    #         <td> </td><td> </td><td> </td></tr>\n"
    #     table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    #     table_html += "<tr><td> </td><td> </td><td> </td><td> </td><td> </td></tr>\n"
    #     table_html += self.create_table_elements(pharmacy_list)

    #     table_html += "</table>\n"

    #     # Get the current date and time
    #     unformatted_datetime = datetime.now()
    #     # Format the date and time
    #     formatted_datetime = unformatted_datetime.strftime("%d:%m:%Y %H:%M:%S")

    #     html_content = f"""
    #     <!DOCTYPE html>
    #     <html>
    #     <head>
    #         <title>{self.html_title}</title>
    #         <meta http-equiv="refresh" content="60">
    #         <meta charset="utf-8">
    #         <link rel="stylesheet" href="./styles.css">
    #     </head>
    #         <body>
    #             <p>Aktuelle Uhrzeit: <span id="time-display"></span></p>

    #             <div style="position: relative;">
    #                 <div style="position: relative; top: 10px; left: 20px;">
    #                     <h1 style="margin-bottom: 100px;">{self.html_title}</h1>
    #                     <img src={self.logo_jpg} style="position: absolute; top: -50px; right: 10px;">
    #                     {table_html}
    #                     <br>
    #                     <p>Generated on {formatted_datetime}</p>

    #                 </div>
    #             </div>
    #             <script>
    #                 function updateTime() {{
    #                     const currentTime = new Date();
    #                     /*
    #                     const options = {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' }};
    #                     */
    #                     const options = {{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' }};

    #                     const timeString = currentTime.toLocaleString('de-DE', options);
    #                     document.getElementById('time-display').textContent = timeString+ ' Uhr';
    #                 }}

    #                 setInterval(updateTime, 1000); // Update the time every second
    #             </script>
    #     </body>
    # </html>
    #     """
    #     with open(self.html_page, "w", encoding="utf-8") as f:
    #         f.write(html_content)

