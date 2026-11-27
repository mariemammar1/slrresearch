
import json
from pathlib import Path

from slrresearch.schemas.article import Article


class ArticleLoader:

    @staticmethod
    def load(filepath="data/raw/search_results.json"):
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(
                f"Article file not found: {filepath}"
            )

        with filepath.open("r", encoding="utf-8") as file:
            data = json.load(file)

        articles = [
            Article.model_validate(item)
            for item in data
        ]

        return articles
