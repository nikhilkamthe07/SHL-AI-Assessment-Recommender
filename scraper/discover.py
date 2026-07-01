from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://www.shl.com"

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


def accept_cookies(page):
    try:
        page.get_by_role(
            "button",
            name="Allow all cookies"
        ).click(timeout=3000)
    except:
        pass


def discover_links():

    urls = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(CATALOG_URL)

        page.wait_for_timeout(3000)

        accept_cookies(page)

        page.wait_for_timeout(3000)

        links = page.locator("a")

        print("Total Links:", links.count())

        for i in range(links.count()):

            href = links.nth(i).get_attribute("href")

            if href and "/products/assessments/" in href:

                if href.startswith("/"):

                    href = BASE_URL + href

                urls.append(href)

        browser.close()

    urls = list(set(urls))

    print(f"\nTotal Assessment URLs Found: {len(urls)}")

    with open("data/urls.json", "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=4)

    print("✅ urls.json created")


if __name__ == "__main__":
    discover_links()