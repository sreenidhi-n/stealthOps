import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

def make_tor_request(url):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies)
        return response
    except ConnectionError as e:
        print("Connection Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def display_directory_urls(response):
    if not response:
        print("No response received.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    if links:
        for link in links:
            href = link.get('href')
            if href and (href.startswith("http://") or href.startswith("https://")):
                print(href)
    else:
        print("No URLs found using <a> tags.")

    all_links = soup.find_all(href=True)
    if all_links:
        for link in all_links:
            href = link.get('href')
            if href and (href.startswith("http://") or href.startswith("https://")):
                print(href)
    else:
        print("No URLs found using href attributes.")

    print("\nHTML Content:\n", soup.prettify())

onion_url = "https://exchanger.infinity.taxi/"
response = make_tor_request(onion_url)
if response and response.status_code == 200:
    display_directory_urls(response)
else:
    print("Failed to retrieve directory listing or status code is not 200.")

