from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest


class TestDeposit:
    def test_deposit_valid(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_response: CreateAccountResponse,
            db_session: Session
    ):
        deposit_request = DepositRequest(accountId=account_response.id, amount=1000)
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        assert response.id == account_response.id
        assert response.balance == 1000

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_response.id)
        assert account_from_db.balance == 1000

        transaction_from_db = TransactionCrudDb.get_last_transaction_by_type(
            db_session,
            transaction_type="deposit",
            to_account_id=account_response.id
        )
        assert transaction_from_db is not None, "Транзакция пополнения не записалась в БД"
        assert transaction_from_db.amount == 1000

    def test_deposit_invalid_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_response: CreateAccountResponse,
            db_session: Session
    ):
        deposit_request = DepositRequest(accountId=account_response.id, amount=999)
        api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account_response.id)
        assert account_from_db.balance == 0
