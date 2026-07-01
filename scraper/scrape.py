from playwright.sync_api import sync_playwright
from utils import accept_cookies


class SHLScraper:

    def __init__(self):

        self.base_url = "https://www.shl.com"

        self.browser = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

    def open(self, url):

        self.page.goto(
            url,
            wait_until="networkidle"
        )

        accept_cookies(self.page)

    def close(self):

        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":

    scraper = SHLScraper()

    scraper.start()

    scraper.open(
        "https://www.shl.com/products/assessments/personality-assessment/shl-occupational-personality-questionnaire-opq/"
    )

    print(scraper.page.title())

    scraper.close()