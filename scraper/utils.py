from playwright.sync_api import Page


def accept_cookies(page: Page):
    """Accept cookie popup if it appears."""

    try:
        page.get_by_role(
            "button",
            name="Allow all cookies"
        ).click(timeout=3000)

        print("✅ Cookies Accepted")

    except:
        print("ℹ️ Cookie popup not found")