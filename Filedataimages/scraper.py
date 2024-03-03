#!/usr/bin/env python3
import requests
from lxml import html, etree
import urllib.parse
import collections
import sys
import re
import os

# Disable SSL warnings
try:
    import urllib3
    urllib3.disable_warnings()
except:
    pass

START = sys.argv[1]
urlq = collections.deque()  
urlq.append(START)  

found = set()  
found.add(START)

# Regular expression pattern to match email addresses
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

# Create a directory to store output files if it doesn't exist
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

# Counter to keep track of the number of files created
files_created = 0

while len(urlq) and files_created < 1:  # Stop after creating one file for each URL
    url = urlq.popleft()

    response = requests.get(url)
    body = html.fromstring(response.content)

    result = etree.tostring(body, encoding='unicode', pretty_print=True, method="html")

    # Extract the filename from the URL
    filename = urllib.parse.urlparse(url).hostname + '.txt'

    # Write the result to a separate file
    output_file = os.path.join(output_dir, filename)
    with open(output_file, 'w') as file:
        file.write(result + '\n')

    # Increment the counter for files created
    files_created += 1

    # Find all links, but make sure we stay on the same site.
    links = {urllib.parse.urljoin(response.url, url) for url in body.xpath('//a/@href') if urllib.parse.urljoin(response.url, url).startswith(START)}

    # Add new URLs to the queue
    for link in (links - found):
        found.add(link)
        urlq.append(link)

    # Find and write email addresses to the output file
    emails = email_pattern.findall(result)
    with open(output_file, 'a') as file:
        for email in emails:
            file.write(email + '\n')

