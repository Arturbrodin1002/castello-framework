from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest


class TestDeposit:
    def test_deposit_valid(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            deposit_request: DepositRequest,
            db_session: Session
    ):
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        assert response.balance == 1000, "После пополнения баланс в ответе должен стать 1000"

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, deposit_request.accountId)
        assert account_from_db.balance == 1000, "После пополнения баланс счета в БД должен стать 1000"

    def test_deposit_invalid_amount(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            invalid_deposit_request: DepositRequest,
            db_session: Session
    ):
        api_manager.user_steps.deposit_invalid(create_user_request, invalid_deposit_request)

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, invalid_deposit_request.accountId)
        assert account_from_db.balance == 0, "После невалидного пополнения баланс счета должен остаться нулевым"
