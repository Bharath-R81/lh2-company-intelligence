import os
import json
from datetime import datetime, timezone

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials


load_dotenv()


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_sheet():
    credentials_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not credentials_file and not credentials_json:
        raise ValueError(
            "Google service account credentials are missing"
        )

    if not sheet_id:
        raise ValueError(
            "GOOGLE_SHEET_ID is missing from .env"
        )

    if credentials_json:
        credentials_info = json.loads(credentials_json)

        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=SCOPES,
        )
    else:
        credentials = Credentials.from_service_account_file(
            credentials_file,
            scopes=SCOPES,
        )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(sheet_id)

    worksheet = spreadsheet.sheet1

    return worksheet


def get_companies():
    worksheet = get_sheet()

    records = worksheet.get_all_records()

    return records


def update_company_result(company_name: str, result: dict):
    worksheet = get_sheet()

    companies = worksheet.get_all_records()

    for row_number, row in enumerate(companies, start=2):
        if row.get("company_name") == company_name:

            processed_at = datetime.now(
                timezone.utc
            ).isoformat()

            worksheet.update(
                range_name=f"C{row_number}:H{row_number}",
                values=[[
                    "JUDGED",
                    result.get("fit", ""),
                    result.get("confidence", ""),
                    result.get("reasoning", ""),
                    result.get("follow_up_question", ""),
                    processed_at,
                ]],
            )

            print(
                f"Google Sheet updated: {company_name}"
            )

            return

    raise ValueError(
        f"Company not found in Google Sheet: {company_name}"
    )


if __name__ == "__main__":
    companies = get_companies()

    print("Google Sheets connection successful!")
    print(f"Companies found: {len(companies)}")

    for company in companies:
        print(company)