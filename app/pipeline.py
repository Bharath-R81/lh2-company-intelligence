from app.google_sheets import (
    get_companies,
    update_company_result,
)
from app.database import (
    save_company,
    update_company_signals,
    update_company_judgment,
)
from app.enrichment import enrich_company
from app.judge import judge_company


def process_company(company: dict):
    company_name = company["company_name"]

    print("\n" + "=" * 60)
    print(f"PROCESSING: {company_name}")
    print("=" * 60)

    try:
        # 1. Save company to database
        print("1. Saving company to database...")
        save_company(company)

        # 2. Collect enrichment signals
        print("2. Collecting enrichment signals...")
        signals = enrich_company(company)

        # 3. Save enrichment signals
        print("3. Saving enrichment signals...")
        update_company_signals(
            company_name,
            signals
        )

        # 4. Run LLM judge
        print("4. Running LLM judge...")
        judgment = judge_company(
            company,
            signals
        )

        # 5. Save judgment to database
        print("5. Saving judgment to database...")
        update_company_judgment(
            company_name,
            judgment
        )

        # 6. Sync result back to Google Sheet
        print("6. Updating Google Sheet...")
        update_company_result(
            company_name,
            judgment
        )

        print(f"\nSUCCESS: {company_name}")
        print(f"Fit: {judgment.get('fit')}")
        print(
            f"Confidence: "
            f"{judgment.get('confidence')}"
        )

        return True

    except Exception as error:
        print(f"\nFAILED: {company_name}")
        print(f"Error: {error}")

        return False


def run_pipeline():
    print("\n" + "=" * 60)
    print("LH2 COMPANY INTELLIGENCE PIPELINE")
    print("=" * 60)

    # Read the Sheet every time the pipeline runs.
    # New rows therefore do not require an application restart.
    companies = get_companies()

    print(
        f"\nFound {len(companies)} companies "
        "in Google Sheet."
    )

    new_companies = [
        company
        for company in companies
        if company.get("status") == "NEW"
    ]

    print(
        f"NEW companies to process: "
        f"{len(new_companies)}"
    )

    if not new_companies:
        print("\nNo NEW companies found.")
        return

    successful = 0
    failed = 0

    for company in new_companies:
        success = process_company(company)

        if success:
            successful += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total processed: {len(new_companies)}")


if __name__ == "__main__":
    run_pipeline()