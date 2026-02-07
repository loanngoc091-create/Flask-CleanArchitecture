class SearchService:
    def __init__(self, uow):
        self.uow = uow

    def search_published(self, keyword=None, major=None, semester=None):
        return self.uow.syllabuses.search_published(
            keyword=keyword,
            major=major,
            semester=semester
        )
