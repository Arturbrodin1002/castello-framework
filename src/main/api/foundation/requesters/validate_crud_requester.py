from typing import Optional
import allure

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(request_spec, endpoint, response_spec)


    def post(self, model: Optional[BaseModel] = None ) -> BaseModel:
        response = self.crud_requester.post(model)

        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())


    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)

        if self.endpoint.value.response_model is None:
            return response

        return self.endpoint.value.response_model.model_validate(response.json())
