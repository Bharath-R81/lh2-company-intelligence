from google_sheets import get_companies
from database import save_company, get_companies as get_database_companies


def main():
    companies = get_companies()

    print(f"Found {len(companies)} companies in Google Sheets.")

    for company in companies:
        save_company(company)
        print(f"Saved: {company['company_name']}")

    database_companies = get_database_companies()

    print("\nCompanies currently in database:")

    for company in database_companies:
        print(
            f"{company['company_name']} - "
            f"{company['website']} - "
            f"{company['status']}"
        )


if __name__ == "__main__":
    main()