from typing import Optional
import json

import requests
import allure
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    def get(self, path_param: Optional[int] = None) -> Response:
        url = f"{Config.fetch("backendUrl")}{self.endpoint.value.url}"
        if path_param is not None:
            url = f"{url}/{path_param}"

        with allure.step(f"GET {url}"):
            response = requests.get(
                url=url,
                headers=self.request_spec
            )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )

        self.response_spec(response)
        return response

    def post(self, model: Optional[BaseModel] = None) ->  Response:
        body = model.model_dump() if model is not None else None
        url = f"{Config.fetch("backendUrl")}{self.endpoint.value.url}"

        with allure.step(f"POST {url}"):
            allure.attach(
                json.dumps(body, ensure_ascii=False, indent=2),
                "Request body",
                allure.attachment_type.JSON
            )

        request_kwargs = {
            "url": url,
            "headers": self.request_spec
        }
        if body is not None:
            request_kwargs["json"] = body

        response = requests.post(**request_kwargs)

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )

        return response


    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
