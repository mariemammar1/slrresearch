import re

class ArticleDeduplicator:

    @staticmethod
    def normalize_doi(doi):

        if not doi:
            return None

        doi = doi.lower().strip()

        doi = doi.replace(
            "https://doi.org/",
            ""
        )

        doi = doi.replace(
            "http://doi.org/",
            ""
        )

        doi = doi.replace(
            "https://dx.doi.org/",
            ""
        )

        doi = doi.replace(
            "http://dx.doi.org/",
            ""
        )

        return doi.strip()

    @staticmethod
    def normalize_title(title):

        if not title:
            return ""

        title = title.lower()

        title = re.sub(
            r"[^a-z0-9]",
            "",
            title
        )

        return title

    @classmethod
    def deduplicate(cls, articles):

        unique_articles = []
        seen_dois = set()
        seen_titles = set()

        for article in articles:

            doi = cls.normalize_doi(
                article.doi
            )

            title = cls.normalize_title(
                article.title
            )

            if doi and doi in seen_dois:
                continue

            if title and title in seen_titles:
                continue

            if doi:
                seen_dois.add(doi)

            if title:
                seen_titles.add(title)

            unique_articles.append(article)

        return unique_articles