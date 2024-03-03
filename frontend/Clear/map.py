#!/usr/bin/env python3
import requests  
from lxml import html, etree
import urllib.parse  
import collections
import sys
import re

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

# Regular expression pattern to match lines containing 'Clearnet'
clearnet_pattern = re.compile(r'.*Clearnet.*', re.MULTILINE)

# Open a file for writing
with open('output.txt', 'w') as file:
    while len(urlq):  
        url = urlq.popleft()

        response = requests.get(url)
        body = html.fromstring(response.content)

        result = etree.tostring(body, encoding='unicode', pretty_print=True, method="html")
        file.write(result + '\n')  # Write the result to the file

        # Find all links, but make sure we stay on the same site.
        links = {urllib.parse.urljoin(response.url, url) for url in body.xpath('//a/@href') if urllib.parse.urljoin(response.url, url).startswith(START)}

        # Add new URLs to list
        for link in (links - found):
            found.add(link)
            urlq.append(link)

        # Find and print email addresses
        emails = email_pattern.findall(result)
        for email in emails:
            file.write(email + '\n')  # Write the email to the file

        # Check for lines containing 'Clearnet' and write them to clearnet.txt
        clearnet_lines = clearnet_pattern.findall(result)
        if clearnet_lines:
            with open('clearnet.txt', 'w') as clearnet_file:
                for line in clearnet_lines:
                    clearnet_file.write(line + '\n')

