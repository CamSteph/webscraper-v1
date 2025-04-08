# Python Web Scraper V1

A simple web scraping project built in Python. This script extracts data from websites and saves it in a structured format. The project is intended to help me learn the basics of web scraping and Python programming, while providing a tool that can be used for website malware reviews.

## Features

- Scrapes data from HTML pages using the `requests` library.
- Extracts specific data points, such as script tags, links, or other elements.
- Saves the scraped data into a SQL database
- Handles basic error checking (e.g., invalid URLs, network errors).

## Installation

Follow these steps to set up the project on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/CamSteph/webscraper-v1.git
   cd webscraper-v1
   ```

2. Create a virtual environment on Linux/macOS (optional):

    ```bash
    virtualenv venv && source venv/bin/activate
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the script

    ```bash
    python scraper.py
    ```

## Dependencies

- `requests` – For sending HTTP requests to retrieve web page content.

## Contributions

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Please make sure to follow the code style used in the project and write tests for new features or fixes.

Made with ❤️ by Cameron Stephenson
