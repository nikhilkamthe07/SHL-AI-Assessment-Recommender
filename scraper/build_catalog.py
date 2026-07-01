import json
from playwright.sync_api import sync_playwright

BASE_DIR = "data"

with open(f"{BASE_DIR}/urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

catalog = []


def accept_cookies(page):
    try:
        page.get_by_role(
            "button",
            name="Allow all cookies"
        ).click(timeout=3000)
    except:
        pass


SKIP_WORDS = [
    "cookie",
    "privacy",
    "browser",
    "advertising",
    "provider",
    "permission",
    "latest browser",
    "modern browser",
    "cookies are small",
    "view our full",
    "allow all cookies",
    "show details",
]


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for url in urls:

        print(f"\nScraping: {url}")

        try:

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            accept_cookies(page)

            page.wait_for_timeout(2000)

            # Assessment Name
            name = page.locator("h1").first.inner_text().strip()

            # Breadcrumb Category
            category = ""
            try:
                breadcrumbs = page.locator("nav a").all_inner_texts()
                if len(breadcrumbs) >= 2:
                    category = breadcrumbs[-1]
            except:
                category = ""

            # Find proper description
            paragraphs = page.locator("p")

            description = ""

            for i in range(paragraphs.count()):

                text = paragraphs.nth(i).inner_text().strip()

                if len(text) < 40:
                    continue

                if any(word in text.lower() for word in SKIP_WORDS):
                    continue

                description = text
                break

            catalog.append(
                {
                    "name": name,
                    "category": category,
                    "url": url,
                    "description": description
                }
            )

            print("✓", name)

        except Exception as e:
            print("❌ Error:", e)

    browser.close()


with open(f"{BASE_DIR}/catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

print("\n✅ catalog.json created successfully!")
print("Total Assessments:", len(catalog))