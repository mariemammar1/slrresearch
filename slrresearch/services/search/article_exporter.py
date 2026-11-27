
import json
from pathlib import Path


class ArticleExporter:

    @staticmethod
    def export(articles, filepath="data/raw/search_results.json"):
        filepath = Path(filepath)

        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Convert Pydantic Article objects into dictionaries
        data = [article.model_dump() for article in articles]

        # Save as JSON
        with filepath.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return filepath
