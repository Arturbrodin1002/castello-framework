from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest


class TestCreditRepay:
    def test_credit_repay_valid(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            db_session: Session
    ):
        credit_response = api_manager.user_steps.request_credit(
            credit_user_request,
            CreditRequest(accountId=credit_account_response.id, amount=5000, termMonths=12)
        )
        repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=credit_account_response.id,
            amount=5000
        )
        response = api_manager.user_steps.repay_credit(credit_user_request, repay_request)

        assert response.creditId == credit_response.creditId
        assert response.amountDeposited == 5000

        account_from_db = AccountCrudDb.get_account_by_id(db_session, credit_account_response.id)
        assert account_from_db.balance == 0

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.balance == 0

        transaction_from_db = TransactionCrudDb.get_last_transaction_by_type(
            db_session,
            transaction_type="credit_repayment",
            from_account_id=credit_account_response.id,
            credit_id=credit_response.creditId
        )
        assert transaction_from_db is not None, "Транзакция погашения кредита не записалась в БД"
        assert transaction_from_db.amount == 5000

    def test_credit_repay_invalid_amount(
            self,
            api_manager: ApiManager,
            credit_user_request: CreateUserRequest,
            credit_account_response: CreateAccountResponse,
            db_session: Session
    ):
        credit_response = api_manager.user_steps.request_credit(
            credit_user_request,
            CreditRequest(accountId=credit_account_response.id, amount=5000, termMonths=12)
        )
        repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=credit_account_response.id,
            amount=1000
        )
        api_manager.user_steps.repay_invalid_credit(credit_user_request, repay_request)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, credit_account_response.id)
        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, credit_response.creditId)
        assert account_from_db.balance == 5000
        assert credit_from_db.balance == -5000
