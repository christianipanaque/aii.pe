import csv
import os
from datetime import datetime


def generate_markdown(data):
    markdown_content = ""

    for row in data:
        # Extract data from the row
        href_src = row["Href Src"]
        href_text = row["Href Text"]
        desc_text = row["Last Span Text"]

        # Format the Markdown content for the row
        markdown_content += (
            '\n### {}\n\n{}\n\n[Read more]({}){{:target="\_blank"}}\n'.format(
                href_text, desc_text, href_src
            )
        )

    return markdown_content.strip()


def save_to_markdown(markdown_content, folder, filename):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate the file path
    filepath = os.path.join(folder, filename)

    # Write Markdown content to the file
    with open(filepath, "w", encoding="utf-8") as markdown_file:
        markdown_file.write(markdown_content)


def main():
    input_csv = "scraped_data.csv"  # Replace this with the path to your CSV file
    output_folder = "_news_posts"
    today_date = datetime.now().strftime("%Y-%m-%d")
    output_filename = "{}.md".format(today_date)

    # Read data from CSV file
    try:
        with open(input_csv, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    except FileNotFoundError:
        print("CSV file '{}' not found.".format(input_csv))
        return

    # Generate Markdown content
    markdown_content = generate_markdown(data)

    # Save Markdown content to file
    save_to_markdown(markdown_content, output_folder, output_filename)
    print(
        "Markdown file '{}' created successfully.".format(
            os.path.join(output_folder, output_filename)
        )
    )


if __name__ == "__main__":
    main()
