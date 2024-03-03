import os
import subprocess

# Path to the input text file containing URLs
input_file = "transactions.txt"

# Read URLs from the input file
with open(input_file, "r") as f:
    urls = f.readlines()

# Remove whitespace characters like `\n` at the end of each line
urls = [url.strip() for url in urls]

# Iterate through each URL and call scrape.py with torify
for url in urls:
    # Command to execute with torify
    command = f"torify ./scraper.py {url}"
    
    # Execute the command in the shell
    subprocess.run(command, shell=True)

