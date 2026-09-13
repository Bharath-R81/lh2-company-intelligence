from google_sheets import get_companies
from enrichment import enrich_company
from database import update_company_signals


def main():
    companies = get_companies()

    for company in companies:
        if company.get("status") != "NEW":
            continue

        company_name = company["company_name"]

        print(f"\nProcessing: {company_name}")

        signals = enrich_company(company)

        update_company_signals(
            company_name,
            signals,
        )

        print(f"Saved enrichment for: {company_name}")


if __name__ == "__main__":
    main()