from webscrapping_to_db import run_linkedin_scraper
from mongodb_communicate import send_notification


if __name__ == "__main__":
    run_linkedin_scraper()
    send_notification()