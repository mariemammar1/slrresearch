
import urllib.parse
import urllib.request
import json


class CrossrefService:

    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str, max_results: int = 10):

        params = {
            "query": query,
            "rows": max_results,
        }

        url = (
            f"{self.BASE_URL}?"
            f"{urllib.parse.urlencode(params)}"
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "SLRResearchAI/1.0"
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=30,
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        return data.get("message", {}).get("items", [])
