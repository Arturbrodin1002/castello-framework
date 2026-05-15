from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest


class TestCreditRequest:
    def test_credit_request_valid(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            db_session: Session
    ):
        credit_request = CreditRequest(accountId=credit_account_response.id, amount=5000, termMonths=12)
        response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        assert response.id == credit_account_response.id
        assert response.amount == 5000
        assert response.termMonths == 12
        assert response.balance == 5000

        account_from_db = AccountCrudDb.get_account_by_id(db_session, credit_account_response.id)
        assert account_from_db.balance == 5000

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db is not None, "Кредит не записался в БД"
        assert credit_from_db.account_id == credit_account_response.id
        assert credit_from_db.amount == 5000
        assert credit_from_db.balance == -5000

        transaction_from_db = TransactionCrudDb.get_last_transaction_by_type(
            db_session,
            transaction_type="credit_issuance",
            to_account_id=credit_account_response.id
        )
        assert transaction_from_db is not None, "Транзакция выдачи кредита не записалась в БД"
        assert transaction_from_db.amount == 5000

    def test_credit_request_invalid_amount(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            db_session: Session
    ):
        credit_request = CreditRequest(accountId=credit_account_response.id, amount=4999, termMonths=12)
        api_manager.user_steps.request_invalid_credit(credit_user_request, credit_request)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, credit_account_response.id)
        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, credit_account_response.id)
        assert account_from_db.balance == 0
        assert credit_from_db is None

    def test_second_credit_request_is_not_allowed(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            db_session: Session
    ):
        credit_request = CreditRequest(accountId=credit_account_response.id, amount=5000, termMonths=12)
        first_response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        api_manager.user_steps.request_second_credit(credit_user_request, credit_request)

        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, credit_account_response.id)
        assert credit_from_db.id == first_response.creditId
        assert CreditCrudDb.count_credits_by_account_id(db_session, credit_account_response.id) == 1
