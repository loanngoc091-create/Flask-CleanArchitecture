import uuid


class RefreshTokenService:

    def generate_refresh_token(self, user):
        return str(uuid.uuid4())
