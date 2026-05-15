import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:

    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password:  str):
        request = LoginUserRequest(username=username, password=password)
        login_response = requests.post(
            f"{Config.fetch('backendUrl')}/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()
        )

        if login_response.status_code == 200:
            response_data = LoginUserResponse(**login_response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return  headers

        raise Exception ("Failed to login")


    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()
