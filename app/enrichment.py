from app.browser import get_browser_signal
from app.external import get_external_signal


def enrich_company(company: dict) -> dict:
    """
    Collect multiple independent signals for one company.
    """

    company_name = company["company_name"]
    website = company["website"]

    print(f"\nEnriching: {company_name}")

    print("  → Collecting browser signal...")
    browser_signal = get_browser_signal(website)

    print("  → Collecting external signal...")
    external_signal = get_external_signal(company_name)

    return {
        "browser": browser_signal,
        "external": external_signal,
    }


if __name__ == "__main__":

    company = {
        "company_name": "Stripe",
        "website": "https://stripe.com",
    }

    signals = enrich_company(company)

    print("\n===== ENRICHMENT RESULT =====")

    print("\nBrowser signal:")
    print("Title:", signals["browser"].get("title"))
    print(
        "Browser automation:",
        signals["browser"].get("browser_automation"),
    )

    print("\nExternal signal:")
    print("Source:", signals["external"].get("source"))
    print("Title:", signals["external"].get("title"))
    print("Summary:", signals["external"].get("summary"))