from domain.repositories.user_repository import UserRepository
from domain.models.user import User
from infrastructure.models.user_model import User as UserModel


class UserRepositoryImpl(UserRepository):

    def __init__(self, session):
        self.session = session

    def get_by_email(self, email: str):

        orm = (
            self.session
            .query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if not orm:
            return None

        return User(
            user_id=orm.user_id,
            email=orm.email,
            password=orm.password,
            role_code=self._get_role_code(orm),
            role_name=self._get_role_name(orm)
        )
    def get_by_id(self, user_id: int):
        orm = (
            self.session
            .query(UserModel)
            .filter(UserModel.user_id == user_id)
            .first()
        )

        if not orm:
            return None

        return User(
            user_id=orm.user_id,
            email=orm.email,
            password=orm.password,
            role_code=self._get_role_code(orm),
            role_name=self._get_role_name(orm)
        )
    def _get_role_name(self, user_orm):
        if not user_orm.roles:
            return None
        return user_orm.roles[0].role.role_name

    def _get_role_code(self, user_orm):
        if not user_orm.roles:
            return None
        return user_orm.roles[0].role.role_code
