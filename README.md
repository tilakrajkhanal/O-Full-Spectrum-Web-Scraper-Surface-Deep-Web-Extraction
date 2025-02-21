# O-Full-Spectrum-Web-Scraper-Surface-Deep-Web-Extraction
A Python-based web scraper designed to extract data from regular websites and .onion domains anonymously via the Tor network. It retrieves metadata, links, emails, and also captures screenshots for verification.

 Overview
This project is a full-spectrum web scraper designed to extract data from both regular websites and .onion sites on the dark web. It leverages Tor for anonymous access, Selenium for JavaScript-heavy sites, and BeautifulSoup for efficient HTML parsing. Additionally, the scraper captures metadata, email addresses, hyperlinks, and even full-page screenshots for verification.

 Features
✅ Scrapes both surface and dark web (.onion) sites
✅ Extracts titles, metadata, emails, and hyperlinks
✅ Uses Selenium to bypass JavaScript-heavy security measures
✅ Implements Tor proxy for anonymous scraping
✅ Stores extracted data in structured JSON format
✅ Captures full-page screenshots for verification
✅ Supports multithreading for faster performance
✅ Bypasses CAPTCHAs & anti-scraping techniques

⚙️ Installation
1️⃣ Install Dependencies
Ensure you have Python 3.x and pip installed, then install required libraries
pip install -r requirements.txt

sudo apt install tor -y
sudo systemctl start tor

sudo apt install firefox-esr geckodriver -y

 Run the Scraper
 python darkwebscraper.py
You'll be prompted to enter a website URL or a search query.


2️⃣ Scraping a Website
Enter website URL or search query: https://example.com:

The scraper will: ✔ Fetch the page
✔ Extract metadata, emails, and links
✔ Capture a screenshot
✔ Save data in the /scraped_data/ folder

3️⃣ Searching the Dark Web
Enter website URL or search query: bitcoin market

The script will: ✔ Search Ahmia & DarkSearch for .onion links
✔ Scrape top results
✔ Store extracted data & screenshots

🔧 Configuration
TOR_PROXY = "socks5h://127.0.0.1:9050"
HEADLESS_MODE = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

📂 Project Structure
O-Full-Spectrum-Web-Scraper/
│── darkwebscraper.py        # Main script
│── config.py                # Configuration settings
│── requirements.txt         # Dependencies
│── scraped_data/            # Extracted data & screenshots
│── README.md                # Documentation

📜 Example Output
Extracted Data (JSON Format)
{
  "metadata": {
    "title": "Example Site",
    "description": "This is a sample description"
  },
  "emails": ["contact@example.com"],
  "links": ["https://anotherpage.com"]
}

👤 Author
Developed by Tilak Raj Khanal
📧 Contact: your.email@example.com








