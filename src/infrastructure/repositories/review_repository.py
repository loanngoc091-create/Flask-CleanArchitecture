class ReviewRepository:

    def __init__(self, session):
        self.session = session

    def add(self, review):
        self.session.add(review)
