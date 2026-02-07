# src/application/services/auth_service.py

from application.dto.auth_query import AuthQuery
from application.dto.result import AuthResult
from domain.repositories.user_repository import UserRepository
from application.services.refresh_token_service import RefreshTokenService
from infrastructure.unit_of_work import UnitOfWork


class AuthService:

    def __init__(self, refresh_token_service, unit_of_work, user_repository):
        self.refresh_token_service = refresh_token_service
        self.uow = unit_of_work
        self.user_repository = user_repository

    def login(self, email, password):
        user = self.user_repository.get_by_email(email)

        if not user:
            return None

        if user.password != password:
            return None

        return user     