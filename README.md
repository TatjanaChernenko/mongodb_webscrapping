# LinkedIn Web Scraping and Email Notification Project

Author: Tatjana Chernenko, 2024

## Overview
This project aims to automate the process of extracting job postings from LinkedIn, storing them in a local MongoDB database, and notifying the user via email about relevant job opportunities. It offers two modes of operation: one-time scraping and continuous scraping.

## Features
- Web scraping of LinkedIn job postings.
- Saving job postings to a MongoDB database.
- Two modes of operation: one-time scraping or continuous scraping.
- Saving job postings to a CSV file.
- Email notification for job postings matching predefined keywords.

## Installation
1. Clone the repository: git clone https://github.com/TatjanaChernenko/mongodb_webscrapping
2. Navigate to the project directory:
cd mongodb_webscrapping
3. Install the required dependencies using pip:
 pip install -r requirements.txt

## Usage
1. Set up a Google Cloud Platform project and obtain credentials for the Gmail API. Refer to the [Gmail API documentation](https://developers.google.com/gmail/api/quickstart) for detailed instructions.
2. Rename the downloaded client secrets file to `client_secret.json` and place it in the project's root directory.
3. Configure the parameters in the `config.ini` file, including your email addresses, LinkedIn search parameters, and other settings.
4. Run the `main.py` file

## Configuration
You can customize the project's behavior by editing the `config.ini` file. Here are the available parameters:
- `email_sender`: Your email address for sending notifications.
- `email_recipient`: Recipient email address for receiving notifications.
- `linkedin_pages`: Number of LinkedIn pages to scrape.
- `keywords`: Keywords to match for suitable job postings.
- `page_number`: Initial page number for scraping.
- `sleep_time`: Time interval between scraping requests.

## License
This project is licensed under the terms of the [MIT License](LICENSE).

## Author
- [Tatjana Chernenko](mailto:tatjana.chernenko.work@gmail.com)



