from src.main.api.models.login_user_request import LoginUserRequest


class TestLogin:

    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, "В ответе вернулся username другого админа"
        assert response.user.role == "ROLE_ADMIN", "Админ авторизовался с некорректной ролью"


    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert response.user.username == create_user_request.username, "В ответе вернулся username другого пользователя"
        assert response.user.role == "ROLE_USER", "Пользователь авторизовался с некорректной ролью"
