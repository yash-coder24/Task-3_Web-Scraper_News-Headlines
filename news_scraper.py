import requests
from bs4 import BeautifulSoup

# CONFIG
URL = "https://indianexpress.com"   # You can change website
OUTPUT_FILE = "headlines.txt"

# FETCH HTML
def fetch_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching website:", e)
        return None

# PARSE HEADLINES
def extract_headlines(html):
    soup = BeautifulSoup(html, "html.parser")

    headlines = []

    # Try multiple tags (works for many sites)
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if text and len(text) > 20:  # Filter small text
            headlines.append(text)

    # Remove duplicates
    return list(set(headlines))


# SAVE TO FILE
def save_to_file(headlines, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for i, headline in enumerate(headlines, 1):
            file.write(f"{i}. {headline}\n")

    print(f"\n✅ Saved {len(headlines)} headlines to {filename}")


# MAIN
def main():
    print("🔍 Fetching news headlines...")

    html = fetch_html(URL)
    if not html:
        return

    headlines = extract_headlines(html)

    if headlines:
        save_to_file(headlines, OUTPUT_FILE)
    else:
        print("No headlines found.")

if __name__ == "__main__":
    main()
