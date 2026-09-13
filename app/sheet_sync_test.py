from google_sheets import update_company_result


def main():
    test_result = {
        "fit": "YES",
        "confidence": 0.95,
        "reasoning": (
            "Test result: company demonstrates "
            "strong software and technology signals."
        ),
        "follow_up_question": (
            "Does the company have active AI "
            "automation initiatives?"
        ),
    }

    update_company_result(
        "NVIDIA",
        test_result,
    )


if __name__ == "__main__":
    main()