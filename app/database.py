import os
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")


engine = create_engine(DATABASE_URL)


def save_company(company):
    query = text("""
        INSERT INTO companies (
            company_name,
            website,
            status
        )
        VALUES (
            :company_name,
            :website,
            :status
        )
        ON CONFLICT (company_name)
        DO UPDATE SET
            website = EXCLUDED.website,
            status = EXCLUDED.status,
            updated_at = now()
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "company_name": company["company_name"],
                "website": company["website"],
                "status": company.get("status", "NEW"),
            },
        )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "company_name": company["company_name"],
                "website": company["website"],
                "status": company.get("status", "NEW"),
            },
        )


def get_companies():
    query = text("""
        SELECT
            id,
            company_name,
            website,
            status,
            fit,
            confidence,
            reasoning,
            follow_up_question,
            created_at,
            updated_at
        FROM companies
        ORDER BY created_at DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [dict(row._mapping) for row in result]

def update_company_signals(company_name: str, signals: dict):
    query = text("""
        UPDATE companies
        SET
            signals = CAST(:signals AS jsonb),
            status = 'ENRICHED',
            updated_at = now()
        WHERE company_name = :company_name
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "company_name": company_name,
                "signals": json.dumps(signals),
            },
        )

def update_company_judgment(
    company_name: str,
    judgment: dict
):
    query = text("""
        UPDATE companies
        SET
            fit = :fit,
            confidence = :confidence,
            reasoning = :reasoning,
            follow_up_question = :follow_up_question,
            status = 'JUDGED',
            updated_at = now()
        WHERE company_name = :company_name
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "company_name": company_name,
                "fit": judgment.get("fit"),
                "confidence": judgment.get("confidence"),
                "reasoning": judgment.get("reasoning"),
                "follow_up_question": judgment.get(
                    "follow_up_question"
                ),
            },
        )