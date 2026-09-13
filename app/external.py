import requests


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"


def get_external_signal(company_name: str) -> dict:
    """
    Find the most relevant Wikipedia page for a company
    and retrieve its summary.
    """

    try:
        search_response = requests.get(
            WIKIPEDIA_API,
            params={
                "action": "query",
                "list": "search",
                "srsearch": f"{company_name} company",
                "format": "json",
                "srlimit": 5,
            },
            headers={
                "User-Agent": "LH2-Company-Intelligence/1.0"
            },
            timeout=15,
        )

        search_response.raise_for_status()

        search_data = search_response.json()

        results = search_data.get("query", {}).get(
            "search", []
        )

        if not results:
            return {
                "source": "Wikipedia",
                "found": False,
                "summary": "",
                "error": "No relevant Wikipedia page found",
            }

        # Pick the first search result.
        page_title = results[0]["title"]

        summary_response = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + requests.utils.quote(
                page_title.replace(" ", "_")
            ),
            headers={
                "User-Agent": "LH2-Company-Intelligence/1.0"
            },
            timeout=15,
        )

        summary_response.raise_for_status()

        data = summary_response.json()

        return {
            "source": "Wikipedia",
            "found": True,
            "title": data.get("title", ""),
            "summary": data.get("extract", ""),
            "url": (
                data.get("content_urls", {})
                .get("desktop", {})
                .get("page", "")
            ),
        }

    except Exception as error:
        return {
            "source": "Wikipedia",
            "found": False,
            "summary": "",
            "error": str(error),
        }


if __name__ == "__main__":

    signal = get_external_signal("Stripe")

    print("External signal collected!")
    print("Source:", signal["source"])
    print("Found:", signal["found"])
    print("Title:", signal.get("title"))
    print("Summary:", signal.get("summary"))
    print("URL:", signal.get("url"))

    if signal.get("error"):
        print("Error:", signal["error"])