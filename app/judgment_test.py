from google_sheets import get_companies
from enrichment import enrich_company
from database import update_company_judgment
from judge import judge_company


def main():
    companies = get_companies()

    for company in companies:
        if company.get("status") != "NEW":
            continue

        company_name = company["company_name"]

        print(f"\nProcessing: {company_name}")

        print("  → Collecting enrichment signals...")
        signals = enrich_company(company)

        print("  → Running LLM judge...")
        judgment = judge_company(company, signals)

        print("  → Saving judgment to database...")
        update_company_judgment(company_name, judgment)

        print(f"  → Saved judgment for {company_name}")
        print(f"     Fit: {judgment['fit']}")
        print(f"     Confidence: {judgment['confidence']}")


if __name__ == "__main__":
    main()