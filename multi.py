import os
import subprocess

input_file = "transactions.txt"

with open(input_file, "r") as f:
    urls = f.readlines()

urls = [url.strip() for url in urls]

for url in urls:
    command = f"torify ./scraper.py {url}"
    subprocess.run(command, shell=True)
