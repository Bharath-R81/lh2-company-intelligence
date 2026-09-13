import json
import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")


client = genai.Client(api_key=API_KEY)


MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
]


def judge_company(company: dict, signals: dict) -> dict:
    """
    Judge a company using collected evidence.

    Automatically tries fallback Gemini models if a model
    temporarily returns a 503 capacity error.
    """

    evidence = {
        "company_name": company["company_name"],
        "website": company["website"],
        "signals": signals,
    }

    prompt = f"""
You are a company-intelligence analyst.

Determine whether this company appears to be a good potential
fit for an AI engineering or automation opportunity.

Reason ONLY from the supplied evidence.

Do not invent facts.
Do not treat missing information as positive evidence.
Clearly distinguish evidence from uncertainty.

Return ONLY valid JSON.

Required JSON fields:

fit:
Must be exactly one of:
"YES", "NO", "UNCERTAIN"

confidence:
A number between 0 and 1.

reasoning:
A concise explanation based on the evidence.

follow_up_question:
One useful question that would reduce the biggest remaining
uncertainty.

Company evidence:

{json.dumps(evidence, indent=2)}
"""

    last_error = None

    for model in MODELS:

        print(f"Trying LLM model: {model}")

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                    },
                )

                result = json.loads(response.text)

                return {
                    "fit": result.get("fit"),
                    "confidence": result.get("confidence"),
                    "reasoning": result.get("reasoning"),
                    "follow_up_question": result.get(
                        "follow_up_question"
                    ),
                    "model": model,
                }

            except Exception as error:

                last_error = error

                print(
                    f"Model {model} failed "
                    f"(attempt {attempt + 1}/2): {error}"
                )

                if attempt == 0:
                    time.sleep(3)

        print(
            f"Falling back from {model}..."
        )

    raise RuntimeError(
        f"All Gemini models failed. Last error: {last_error}"
    )


if __name__ == "__main__":

    company = {
        "company_name": "Stripe",
        "website": "https://stripe.com",
    }

    signals = {
        "browser": {
            "title": "Stripe | Financial Infrastructure",
            "visible_text": (
                "Financial infrastructure to grow your revenue. "
                "Accept payments and build financial products."
            ),
            "browser_automation": True,
        },
        "external": {
            "source": "Wikipedia",
            "title": "Stripe, Inc.",
            "summary": (
                "Stripe is a financial services and software "
                "company providing payment processing software "
                "and APIs."
            ),
        },
    }

    result = judge_company(company, signals)

    print("\nLLM Judge successful!")

    print(
        json.dumps(
            result,
            indent=2,
        )
    )