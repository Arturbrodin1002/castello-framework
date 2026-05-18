from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()

        return response

    def create_invalid_account(self, create_user_request: CreateUserRequest, response_spec=None):
        CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            response_spec or ResponseSpecs.request_conflict()
        ).post()

    def get_account_transactions(self, create_user_request: CreateUserRequest, account_id: int):
        response = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_ok()
        ).get(account_id)

        return response.json()

    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)

        return response

    def deposit_invalid(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest, response_spec=None):
        CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT,
            response_spec or ResponseSpecs.request_bad()
        ).post(deposit_request)

    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)

        return response

    def transfer_invalid(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest, response_spec=None):
        CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            response_spec or ResponseSpecs.request_unprocessable()
        ).post(transfer_request)

    def request_credit(self, create_user_request: CreateUserRequest, credit_request: CreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)

        return response

    def request_invalid_credit(self, create_user_request: CreateUserRequest, credit_request: CreditRequest, response_spec=None):
        CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            response_spec or ResponseSpecs.request_bad()
        ).post(credit_request)

    def request_second_credit(self, create_user_request: CreateUserRequest, credit_request: CreditRequest, response_spec=None):
        CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            response_spec or ResponseSpecs.request_not_found()
        ).post(credit_request)

    def repay_credit(self, create_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        return response

    def repay_invalid_credit(
            self,
            create_user_request: CreateUserRequest,
            credit_repay_request: CreditRepayRequest,
            response_spec=None
    ):
        CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REPAY,
            response_spec or ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)
