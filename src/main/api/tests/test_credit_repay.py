from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_response import CreditRequestResponse


class TestCreditRepay:
    def test_credit_repay_valid(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            credit_response: CreditRequestResponse,
            credit_repay_request: CreditRepayRequest,
            db_session: Session
    ):
        response = api_manager.user_steps.repay_credit(credit_user_request, credit_repay_request)

        assert response.amountDeposited == 5000, "Сумма погашения кредита в ответе должна быть 5000"

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, credit_account_response.id)
        credit_from_db = CreditCrudDb.get_required_credit_by_id(db_session, credit_response.creditId)
        assert account_from_db.balance == 0, "После полного погашения баланс счета в БД должен стать нулевым"
        assert credit_from_db.balance == 0, "После полного погашения долг по кредиту в БД должен стать нулевым"

    def test_credit_repay_invalid_amount(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            credit_response: CreditRequestResponse,
            invalid_credit_repay_request: CreditRepayRequest,
            db_session: Session
    ):
        api_manager.user_steps.repay_invalid_credit(credit_user_request, invalid_credit_repay_request)

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, credit_account_response.id)
        credit_from_db = CreditCrudDb.get_required_credit_by_id(db_session, credit_response.creditId)
        assert account_from_db.balance == 5000, "После невалидного погашения баланс счета должен остаться 5000"
        assert credit_from_db.balance == -5000, "После невалидного погашения долг по кредиту должен остаться -5000"
