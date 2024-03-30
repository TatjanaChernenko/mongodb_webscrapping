import configparser
from pymongo import MongoClient
import csv
from email.mime.text import MIMEText
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError


def connect_to_mongodb(config):
    client = MongoClient(config['MongoDB']['uri'])
    db = client[config['MongoDB']['database']]
    collection = db[config['MongoDB']['collection']]
    return collection


def send_email(to_email, subject, body, config):
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)

    from_email = config['EMAIL']['sender_email']
    msg = MIMEText(body)
    msg['From'] = from_email
    msg['to'] = to_email
    msg['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
    try:
        msg = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {msg} Message Id: {msg["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        msg = None


def update_csv(jobs):
    with open('jobs.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for job in jobs:
            if "suitable" not in job.get("metadata", []):
                writer.writerow([job["title"], job["company"], job["location"], job["link"], "suitable"])


def send_notification():
    # Load configuration from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    collection = connect_to_mongodb(config)
    all_jobs = collection.find()
    for job in all_jobs:
        print(job)

    total_jobs = collection.count_documents({})
    print("Total jobs:", total_jobs)

    # example
    jobs_in_SF = collection.find({'location': 'San Francisco, CA'})
    print("Jobs in San Francisco:")
    for job in jobs_in_SF:
        print(job)

    # example
    jobs_at_Google = collection.find({'сompany': 'Google'})
    print("Jobs at Google:")
    for job in jobs_at_Google:
        print(job)

    keywords = config['SCRAPER']['keywords'].split(', ')

    query = {
        "$or": [
            {"location": "Heidelberg"},
            {"title": {"$regex": "|".join(keywords), "$options": "i"}}
        ]
    }
    suitable = collection.find(query)
    suitable_jobs = []
    print("Suitable jobs: ")
    for result in suitable:
        if "suitable" not in result.get("metadata", []):
            suitable_jobs.append(result)
            collection.update_one({"_id": result["_id"]}, {"$push": {"metadata": "suitable"}})
            update_csv(suitable_jobs)

    if suitable_jobs:
        subject = "Suitable job vacancies found"
        body = "The following suitable job vacancies have been found:\n\n"
        for job in suitable_jobs:
            body += f"Title: {job['title']}\nCompany: {job['company']}\nLink: {job['link']}\n\n"
        send_email(config['EMAIL']['recipient_email'], subject, body, config)
        print("Email sent")


if __name__ == "__main__":
    send_notification()
