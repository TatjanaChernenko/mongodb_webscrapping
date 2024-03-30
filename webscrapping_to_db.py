import csv
import configparser
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from datetime import datetime
import logging


def run_linkedin_scraper():
    # Load configuration from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Connect to MongoDB
    client = MongoClient(config['MongoDB']['uri'])
    db = client[config['MongoDB']['database']]
    collection = db[config['MongoDB']['collection']]

    # Open CSV file for writing
    csv_file = open('linkedin-jobs.csv', 'a', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)

    # CSV file headers
    csv_writer.writerow(['Title', 'Company', 'Location', 'Apply'])

    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Create a handler for logging to both console and file
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('scraper.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Scraper function
    def linkedin_scraper(webpage, page_number):
        next_page = webpage + str(page_number)
        logging.info("Scraping: %s", next_page)
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = soup.find_all('div',
                             class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

        new_jobs_count = 0
        for job in jobs:
            job_title = job.find('h3', class_='base-search-card__title').text.strip()
            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find('span', class_='job-search-card__location').text.strip()
            job_link = job.find('a', class_='base-card__full-link')['href']

            # Check if job is already in the database
            if collection.count_documents({'title': job_title, 'company': job_company, 'location': job_location}) == 0:
                # If job is not in the database, add it and write to CSV
                collection.insert_one(
                    {'title': job_title, 'company': job_company, 'location': job_location, 'link': job_link,
                     'timestamp': datetime.now()})
                csv_writer.writerow([job_title, job_company, job_location, job_link])
                logging.info("New job found and added: %s", job_title)
                new_jobs_count += 1

        if page_number < int(config['SCRAPER']['page_number']):
            page_number += int(config['SCRAPER']['page_number'])
            linkedin_scraper(webpage, page_number)

        return new_jobs_count

    # Choose mode of operation (continuous scraping or one-time scraping)
    mode = input("Choose operation mode (1 - continuous scraping, 2 - one-time scraping): ")

    if mode == '1':
        # Continuous scraping with 3-minute interval
        total_jobs = 0
        while True:
            new_jobs_count = linkedin_scraper(
                'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Product%20Management&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=',
                0)
            total_jobs += new_jobs_count
            logging.info("Total jobs in database: %s", collection.count_documents({}))
            logging.info("New jobs added in this session: %s", new_jobs_count)
            logging.info("Total new jobs added: %s", total_jobs)
            logging.info("Timestamp: %s", datetime.now())
            csv_file.flush()
            time.sleep(int(config['SCRAPER']['sleep_time']))

    else:
        # One-time scraping
        linkedin_scraper(
            'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Product%20Management&location=San%20Francisco%20Bay%20Area&geoId=90000084&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=',
            0)
        logging.info("Total jobs in database: %s", collection.count_documents({}))


if __name__ == "__main__":
    run_linkedin_scraper()
