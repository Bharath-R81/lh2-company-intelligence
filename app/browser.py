from playwright.sync_api import sync_playwright


def get_browser_signal(url: str) -> dict:
    """
    Visit a company website using a real browser and
    extract information visible to the browser.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            ),
            viewport={
                "width": 1280,
                "height": 900,
            },
        )

        page = context.new_page()

        try:
            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            # Give the page a moment to render.
            page.wait_for_timeout(2000)

            title = page.title()

            visible_text = page.locator("body").inner_text(
                timeout=10000
            )

            visible_text = " ".join(
                visible_text.split()
            )

            return {
                "url": page.url,
                "status_code": (
                    response.status if response else None
                ),
                "title": title,
                "visible_text": visible_text[:5000],
                "browser_automation": True,
            }

        except Exception as error:

            return {
                "url": page.url,
                "status_code": None,
                "title": "",
                "visible_text": "",
                "browser_automation": True,
                "error": str(error),
            }

        finally:
            browser.close()


if __name__ == "__main__":

    test_url = "https://stripe.com"

    signal = get_browser_signal(test_url)

    print("Browser enrichment completed!")
    print("URL:", signal["url"])
    print("Status code:", signal["status_code"])
    print("Title:", signal["title"])
    print(
        "Browser automation:",
        signal["browser_automation"],
    )

    print("\nVisible page content:")
    print(signal["visible_text"][:1500])

    if signal.get("error"):
        print("\nError:")
        print(signal["error"])