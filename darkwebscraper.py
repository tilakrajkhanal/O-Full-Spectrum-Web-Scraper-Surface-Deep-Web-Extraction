import os
import re
import time
import json
import requests
import socks
import socket
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from shutil import which
from urllib.parse import urlparse

# Tor Proxy Configuration
TOR_SOCKS_PROXY = "socks5h://127.0.0.1:9050"

# Ensure Geckodriver is correctly installed
GECKODRIVER_PATH = which("geckodriver") or "/usr/local/bin/geckodriver"
if not os.path.exists(GECKODRIVER_PATH):
    print("[✘] ERROR: Geckodriver not found! Install it: `sudo apt install -y firefox-esr geckodriver`")
    exit(1)

# Ensure Tor is running
def check_tor():
    try:
        response = requests.get("https://check.torproject.org/", proxies={"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}, timeout=10)
        if "Congratulations" in response.text:
            print("[✔] Tor is running!")
            return True
    except requests.exceptions.RequestException:
        print("[✘] ERROR: Tor is NOT running. Start it with: sudo systemctl start tor")
    return False

# Take screenshot using Firefox (Geckodriver)
def take_screenshot(url):
    screenshot_path = "scraped_data/screenshots/"
    os.makedirs(screenshot_path, exist_ok=True)

    try:
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.set_preference("network.proxy.type", 1)
        options.set_preference("network.proxy.socks", "127.0.0.1")
        options.set_preference("network.proxy.socks_port", 9050)

        driver = webdriver.Firefox(service=FirefoxService(GECKODRIVER_PATH), options=options)
        print(f"[📸] Taking screenshot of {url} ...")

        driver.get(url)
        time.sleep(5)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{screenshot_path}screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"[✔] Screenshot saved as {screenshot_name}")

    except Exception as e:
        print(f"[✘] Failed to capture screenshot: {e}")

    finally:
        try:
            driver.quit()
        except:
            pass

# Extract data from HTML
def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else "No Title Found"
    description = soup.find("meta", attrs={"name": "description"})
    description = description["content"] if description else "No Description Found"
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)
    links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http")]

    return {
        "metadata": {"title": title, "description": description},
        "emails": emails,
        "links": links
    }

# Fetch webpage content
def fetch_url(url, session):
    try:
        response = session.get(url, proxies={"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY} if ".onion" in url else {}, timeout=60, verify=False)
        if response.status_code == 200:
            print(f"[✔] Successfully scraped: {url}")
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"[✘] Error fetching {url}: {e}")
    return None

# Scrape a website and save the extracted data in `scraped_data/`
def scrape_website(url):
    session = requests.Session()
    if ".onion" in url:
        if not check_tor():
            return
        print(f"[+] Connecting to {url} via TOR...")
        session.proxies = {"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}

    page_content = fetch_url(url, session)
    if not page_content:
        return None

    take_screenshot(url)

    data = extract_data(page_content)

    # Generate unique filename for each scrape
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace(".", "_")  # Convert domain for filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"scraped_data/{timestamp}_{domain}.json"

    os.makedirs("scraped_data", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[✔] Extracted data saved to {filename}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda link: fetch_url(link, session), data["links"][:10])

    return data

# Search dark web for .onion links
def search_dark_web(query):
    search_urls = [
        f"https://ahmia.fi/search/?q={query}",
        f"https://phobos.darksearch.io/api/v1/search?q={query}"
    ]
    results = []
    for search_url in search_urls:
        try:
            res = requests.get(search_url, timeout=10)
            links = re.findall(r"http://[a-z2-7]{16,56}\.onion", res.text)
            results.extend(links)
        except:
            continue
    print(f"[+] Dark Web search completed. Found {len(results)} results.")
    return results

if __name__ == "__main__":
    url = input("Enter website URL or search query: ").strip()

    if url.startswith("http://") or url.startswith("https://"):
        if ".onion" in url:
            check_tor()
        scrape_website(url)
    else:
        print("[🔍] Searching Dark Web for:", url)
        found_links = search_dark_web(url)
        if found_links:
            for onion_site in found_links[:3]:
                scrape_website(onion_site)
        else:
            print("[⚠] No onion links found for search query.")

