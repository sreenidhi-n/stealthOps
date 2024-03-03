#!/usr/bin/env python3
import requests  
from lxml import html, etree
import urllib.parse  
import collections
import sys
import re
import os
import csv
from dark_web_scraper import find_images_from_onion_link, find_onion_links

# Disable SSL warnings
try:
    import urllib3
    urllib3.disable_warnings()
except:
    pass

# Regular expression patterns to match email addresses and phone numbers
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
phone_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-2xx responses
        body = html.fromstring(response.content)
        result = etree.tostring(body, encoding='unicode', pretty_print=True, method="html")

        # Find all links, but make sure we stay on the same site.
        links = {urllib.parse.urljoin(response.url, url) for url in body.xpath('//a/@href') if urllib.parse.urljoin(response.url, url).startswith(url)}

        # Find email addresses and phone numbers
        emails = email_pattern.findall(result)
        phones = phone_pattern.findall(result)

        return links, emails, phones

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching data from {url}: {e}")
        return set(), [], []  # Return empty sets and lists to indicate no data retrieved


def create_csv(directory, data):
    csv_file = os.path.join(directory, directory.split("/")[-1] + ".csv")
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Links", "Emails", "Phone Numbers"])
        csvwriter.writerows(data)

def main():
    input_file = "links.txt"

    with open(input_file, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        links, emails, phones = extract_data(url)

        # Create directory for the URL
        directory_name = url.replace('http://', '').replace('https://', '').replace('.onion', '').replace('/', '_')
        os.makedirs(directory_name, exist_ok=True)

        # Store images from onion link
        images = find_images_from_onion_link(url)

        # Combine all data
        data = [(url, ','.join(emails), ','.join(phones))]
        for link in links:
            data.append((link, "", ""))  # Add empty strings for emails and phones as these are not extracted for links

        # Write data to CSV
        create_csv(directory_name, data)

if __name__ == "__main__":
    main()

