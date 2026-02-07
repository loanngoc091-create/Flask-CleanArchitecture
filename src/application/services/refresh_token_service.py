# src/application/services/refresh_token_service.py

import uuid
from domain.models.user import User


class RefreshTokenService:

    def __init__(self, unit_of_work):
        self.uow = unit_of_work

    def save(self, user_id, refresh_token):
        pass
