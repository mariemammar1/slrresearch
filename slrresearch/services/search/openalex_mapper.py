
from slrresearch.schemas.article import Article


class OpenAlexMapper:

    @staticmethod
    def reconstruct_abstract(inverted_index):

        if not inverted_index:
            return None

        words = []

        for word, positions in inverted_index.items():

            for position in positions:

                words.append((position, word))

        words.sort(key=lambda item: item[0])

        return " ".join(
            word for position, word in words
        )

    @classmethod
    def map_article(cls, raw_article):

        authors = []

        for authorship in raw_article.get(
            "authorships", []
        ):

            author = authorship.get(
                "author", {}
            )

            name = author.get("display_name")

            if name:
                authors.append(name)

        abstract = cls.reconstruct_abstract(
            raw_article.get(
                "abstract_inverted_index"
            )
        )

        doi = raw_article.get("doi")

        article = Article(
            title=raw_article.get("title") or "Untitled",
            authors=authors,
            year=raw_article.get("publication_year"),
            doi=doi,
            abstract=abstract,
            source="OpenAlex",
            url=raw_article.get("id"),
        )

        return article
