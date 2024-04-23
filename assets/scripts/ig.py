# BeautifulSoup - parse HTML and XML documents.
from bs4 import BeautifulSoup

# selenium - control a chromedriver browser
# to automate web-based tasks.
from selenium.webdriver.common.by import By

# re - extract data using conditional,
# multiline and group pattern matching using regex
import re

# csv - read from and write to csv files,
# access values by column name.
import csv

# requests - send HTTP requests, headers, SSL,
# session objects, url parameters, JSON decoder,
# timeouts, exceptions, redirections,
# proxies support, authentication and pooling.
import requests


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# List of URLs to scrape
urls = [
    "http://example.com/match1",
    "http://example.com/match2",
    # Add more URLs as needed
]

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Placeholder for scraped data
matches_data = []


for url in urls:
    # Use Requests and Beautiful Soup for static content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extracting match title
    match_title = soup.find("h1", class_="match-title").get_text(strip=True)

    # Use Regular Expressions within Beautiful Soup for specific patterns
    score = re.search(r"(\d+) - (\d+)", match_title)
    if score:
        home_score, away_score = score.groups()

    # Use Selenium for dynamic content
    driver.get(url)
    # Example: Getting dynamically loaded comments count
    # Adjust the selector based on the actual structure of your target website
    comments_count_element = driver.find_element(By.CSS_SELECTOR, ".comments-count")
    comments_count = comments_count_element.text if comments_count_element else "0"

    matches_data.append(
        {
            "title": match_title,
            "home_score": home_score,
            "away_score": away_score,
            "comments_count": comments_count,
        }
    )

driver.quit()

# Write the data to a CSV file
with open("soccer_matches.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["title", "home_score", "away_score", "comments_count"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for match in matches_data:
        writer.writerow(match)
print("Data has been written to soccer_matches.csv")
