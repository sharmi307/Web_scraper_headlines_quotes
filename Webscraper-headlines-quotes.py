
import requests
from bs4 import BeautifulSoup
import csv

URL = "https://quotes.toscrape.com/"

def scrape_quotes():
    try:
        response = requests.get(
            URL,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for item in soup.select(".quote"):
            quote = item.select_one(".text")
            author = item.select_one(".author")
            tags = item.select(".tag")

            results.append({
                "Quote": quote.get_text(strip=True),
                "Author": author.get_text(strip=True),
                "Tags": ", ".join(
                    tag.get_text(strip=True) for tag in tags
                )
            })

        return results

    except requests.RequestException as error:
        print("Unable to access website:", error)
        return []


def save_to_csv(results):
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        fields = ["Quote", "Author", "Tags"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("\nSaved results to quotes.csv")


def main():
    print("=== WEB SCRAPER: QUOTES ===")
    results = scrape_quotes()

    if not results:
        print("No quotes found. Please try again later.")
        return

    for number, item in enumerate(results, start=1):
        print(f"\n{number}. {item['Quote']}")
        print("Author:", item["Author"])
        print("Tags:", item["Tags"])

    print(f"\nTotal quotes scraped: {len(results)}")
    save_to_csv(results)


if __name__ == "__main__":
    main()
