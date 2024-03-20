import csv
import os
from datetime import datetime


def read_csv(filename):
    data = []
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


# Function to generate a unique filename with suffix
def generate_unique_filename(folder_path, base_filename):
    filename = base_filename
    suffix = 1
    while os.path.exists(os.path.join(folder_path, f"{filename}.html")):
        filename = f"{base_filename}_{suffix:03d}"
        suffix += 1
    print(filename)
    return f"{folder_path}/{filename}.html"


def insert_html_blocks(template_file, data):
    # Read content from template HTML file
    with open(template_file, "r", encoding="utf-8") as f:
        template_content = f.read()

    title = "Artificial Intelligence Institute of Peru Newsletter"
    description = "Artificial Intelligence Institute of Peru Newsletter"

    # Create HTML blocks
    html_blocks = ""
    for row in data:
        if " AI " in row["Href Text"]:
            title = row["Href Text"]
            description = f"{row['Last Span Text']}.. Read more"
        html_blocks += (
            f"<div>\n"
            f'<h3>{row["Href Text"]}</h3>\n'
            f'<p>{row["Last Span Text"]}</p>\n'
            f'<p><a href="{row["Href Src"]}" target="_blank">Read more</a></p>\n'
            f"</div>\n\n"
        )
    # replace head title description
    title_placeholder = f"@@@title@@@"
    description_placeholder = f"@@@description@@@"
    html_content = template_content.replace(title_placeholder, title)
    html_content = html_content.replace(description_placeholder, description)

    # Replace placeholder with today's date
    date_placeholder = "<!-- date -->"
    today_date = datetime.today().strftime("%A, %B %d, %Y")
    html_content = html_content.replace(date_placeholder, today_date)

    # Replace placeholder with HTML blocks
    placeholder = "<!-- insert articles here -->"
    if placeholder not in html_content:
        print("Error: Placeholder for articles not found in template HTML file.")
        return

    html_content = html_content.replace(placeholder, html_blocks)

    # Get today's date in "YYYY-MM-DD" format
    today_date = datetime.today().strftime("%Y-%m-%d")
    front_matter = f"---\ndate: {today_date}\npermalink: news/{today_date}\n---\n\n"

    # Create new HTML file with today's date as the filename
    new_html_file = f"_news_posts/{today_date}.html"
    if os.path.exists(new_html_file):
        new_html_file = generate_unique_filename("_news_posts", today_date)

    with open(new_html_file, "w", encoding="utf-8") as f:
        f.write(front_matter + html_content)

    print(f"New HTML file '{new_html_file}' created successfully.")


def main():
    today_date = datetime.now().strftime("%Y-%m-%d")
    csv_file = f"_data_csv/{today_date}_scraped_data.csv"  # Replace with the path to your CSV file
    # csv_file = "scraped_data.csv"
    template_file = "assets/templates/email_002.html"  # Replace with the path to your template HTML file

    # Read data from CSV file
    data = read_csv(csv_file)

    # Insert HTML blocks into template and create new HTML file
    insert_html_blocks(template_file, data)


if __name__ == "__main__":
    main()
