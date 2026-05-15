from typing import Dict, Callable


class HttpRequester:
    def __init__(self, request_spec: Dict, endpoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec

