from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_request_response import CreditRequestResponse


class TestCreditRequest:
    def test_credit_request_valid(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            credit_request: CreditRequest,
            db_session: Session
    ):
        response = api_manager.user_steps.request_credit(credit_user_request, credit_request)

        assert response.balance == 5000, "После выдачи кредита баланс счета в ответе должен стать 5000"

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, credit_account_response.id)
        credit_from_db = CreditCrudDb.get_required_credit_by_id(db_session, response.creditId)
        assert account_from_db.balance == 5000, "После выдачи кредита баланс счета в БД должен стать 5000"
        assert credit_from_db.balance == -5000, "После выдачи кредита долг в БД должен стать -5000"

    def test_credit_request_invalid_amount(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            invalid_credit_request: CreditRequest,
            db_session: Session
    ):
        api_manager.user_steps.request_invalid_credit(credit_user_request, invalid_credit_request)

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, credit_account_response.id)
        credit_from_db = CreditCrudDb.get_credit_by_account_id(db_session, credit_account_response.id)
        assert account_from_db.balance == 0, "После невалидного кредита баланс счета должен остаться нулевым"
        assert credit_from_db is None, "Невалидный кредит не должен записываться в БД"

    def test_second_credit_request_is_not_allowed(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_response: CreditRequestResponse,
            credit_account_response: CreateAccountResponse,
            credit_request: CreditRequest,
            db_session: Session
    ):
        api_manager.user_steps.request_second_credit(credit_user_request, credit_request)

        credit_from_db = CreditCrudDb.get_required_credit_by_account_id(db_session, credit_account_response.id)
        assert credit_from_db.id == credit_response.creditId, "Повторная заявка не должна заменять первый кредит"
        assert CreditCrudDb.count_credits_by_account_id(db_session, credit_account_response.id) == 1, "На один счет нельзя создать больше одного кредита"
