import sys
import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime


def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all tables on the page
        tables = soup.find_all("table")

        # Find the position of the 4th last table
        stop_table_index = max(len(tables) - 4, 0)

        # Find all divs with class="text-block" but exclude those within the last 4 tables
        divs = []
        tables_count = 0
        for element in soup.find_all(["div", "table"]):
            if element.name == "table":
                tables_count += 1
                if tables_count > stop_table_index:
                    break
            elif element.name == "div" and "text-block" in element.get("class", []):
                # Check if the text value contains the word "sponsor" in any case
                text = element.get_text().lower()
                if "sponsor" in text:
                    continue
                divs.append(element)

        scraped_data = []

        # Iterate over each div
        for div in divs:
            # Find the first href link tag and retrieve the src value
            href_link = div.find("a", href=True)
            if href_link:
                href_src = href_link["href"]
                # Retrieve the text value from the href link tag
                href_text = href_link.text.strip()
            else:
                # If no href link tag is found, skip this div
                continue

            # Find the last span element and retrieve the text inside it
            last_span = div.find_all("span")[-1] if div.find_all("span") else None
            if last_span:
                last_span_text = last_span.text.strip()
            else:
                # If no span element is found, skip this div
                continue

            # Store the extracted data in a tuple
            scraped_data.append((href_src, href_text, last_span_text))

        return scraped_data
    else:
        print("Failed to retrieve website. Status code:", response.status_code)
        return None


def save_to_csv(data, filename, folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate the file path
    filepath = os.path.join(folder, filename)

    # Open a CSV file in write mode
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow(["Href Src", "Href Text", "Last Span Text"])

        # Write data to CSV file
        writer.writerows(data)

        print("Data saved to", filepath)


# Main function
def main():
    # Retrieve URL from terminal prompt
    if len(sys.argv) < 2:
        print("Please provide the URL of the website you want to scrape.")
        return
    url = sys.argv[1]

    today_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_date}_scraped_data.csv"  # CSV file to save the extracted data
    output_folder = "_data_csv"

    # Scrape the website
    scraped_data = scrape_website(url)

    # Check if extraction was successful
    if scraped_data:
        # Save extracted data to CSV file
        save_to_csv(scraped_data, filename, output_folder)
    else:
        print("Failed to scrape website.")


if __name__ == "__main__":
    main()
