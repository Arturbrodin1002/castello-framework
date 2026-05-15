import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb


class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(
            self, api_manager,
            create_user_request,
            db_session
    ):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is not None, "Созданного пользователя нет в БД"
        assert user_from_db.username == create_user_request.username, "Созданного пользователя нет в БД "

        users = api_manager.admin_steps.get_users()
        assert any(user["username"] == create_user_request.username for user in users)

    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Max1!", "Pas!sw0rд"),
            ("Max2!", "Pas!sw0"),
            ("Max3!", "pas!sw0d"),
            ("Max4!", "Passw0rd"),
            ("Max5!", "Passw!rd")
        ]
    )
    def test_create_user_invalid(self, username, password, api_manager, db_session):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = UserCrudDb.get_user_by_username(db_session, create_user_request.username)

        assert user_from_db is None, "Пользователь создан, ошибка"
