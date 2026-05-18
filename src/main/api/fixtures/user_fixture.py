import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def second_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def account_response(api_manager, create_user_request) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def second_account_response(api_manager, second_user_request) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(second_user_request)


@pytest.fixture
def credit_account_response(api_manager, credit_user_request) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(credit_user_request)


@pytest.fixture
def deposit_request(account_response: CreateAccountResponse) -> DepositRequest:
    return DepositRequest(accountId=account_response.id, amount=1000)


@pytest.fixture
def invalid_deposit_request(account_response: CreateAccountResponse) -> DepositRequest:
    return DepositRequest(accountId=account_response.id, amount=999)


@pytest.fixture
def funded_account_response(api_manager, create_user_request, account_response, deposit_request) -> CreateAccountResponse:
    api_manager.user_steps.deposit(create_user_request, deposit_request)
    return account_response


@pytest.fixture
def transfer_request(
        funded_account_response: CreateAccountResponse,
        second_account_response: CreateAccountResponse
) -> TransferRequest:
    return TransferRequest(
        fromAccountId=funded_account_response.id,
        toAccountId=second_account_response.id,
        amount=500
    )


@pytest.fixture
def invalid_transfer_request(
        account_response: CreateAccountResponse,
        second_account_response: CreateAccountResponse
) -> TransferRequest:
    return TransferRequest(
        fromAccountId=account_response.id,
        toAccountId=second_account_response.id,
        amount=500
    )


@pytest.fixture
def transfer_history_response(api_manager, create_user_request, second_user_request, transfer_request):
    api_manager.user_steps.transfer(create_user_request, transfer_request)
    sender_history = api_manager.user_steps.get_account_transactions(
        create_user_request,
        transfer_request.fromAccountId
    )
    receiver_history = api_manager.user_steps.get_account_transactions(
        second_user_request,
        transfer_request.toAccountId
    )
    return sender_history, receiver_history


@pytest.fixture
def credit_request(credit_account_response: CreateAccountResponse) -> CreditRequest:
    return CreditRequest(accountId=credit_account_response.id, amount=5000, termMonths=12)


@pytest.fixture
def invalid_credit_request(credit_account_response: CreateAccountResponse) -> CreditRequest:
    return CreditRequest(accountId=credit_account_response.id, amount=4999, termMonths=12)


@pytest.fixture
def credit_response(api_manager, credit_user_request, credit_request) -> CreditRequestResponse:
    return api_manager.user_steps.request_credit(credit_user_request, credit_request)


@pytest.fixture
def credit_repay_request(credit_response, credit_account_response: CreateAccountResponse) -> CreditRepayRequest:
    return CreditRepayRequest(
        creditId=credit_response.creditId,
        accountId=credit_account_response.id,
        amount=5000
    )


@pytest.fixture
def invalid_credit_repay_request(credit_response, credit_account_response: CreateAccountResponse) -> CreditRepayRequest:
    return CreditRepayRequest(
        creditId=credit_response.creditId,
        accountId=credit_account_response.id,
        amount=1000
    )


@pytest.fixture
def account_with_two_accounts(api_manager, create_user_request):
    api_manager.user_steps.create_account(create_user_request)
    api_manager.user_steps.create_account(create_user_request)
    return create_user_request
