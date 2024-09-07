import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import time

def extract_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        return [urljoin(url, link.get('href')) for link in links if link.get('href')]
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return []

def save_links_to_file(links, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(f"{link}\n")

def extract_and_save_links(start_url, output_file):
    visited = set()
    to_visit = set([start_url])
    all_links = set()

    while to_visit:
        current_url = to_visit.pop()
        if current_url not in visited:
            print(f"Extracting links from {current_url}...")
            links = extract_links(current_url)
            visited.add(current_url)

            for link in links:
                if link.startswith(start_url):
                    if '/comments/' in link:
                        all_links.add(link)
                    if link not in visited:
                        to_visit.add(link)
        
        time.sleep(1)  # Respect the website's server by adding a delay

    save_links_to_file(all_links, output_file)
    print(f"Links saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all post links from a subreddit and save them to a file.")
    parser.add_argument("url", help="The starting URL to extract links from")
    parser.add_argument("output", help="The output file name to save the links")

    args = parser.parse_args()

    extract_and_save_links(args.url, args.output)