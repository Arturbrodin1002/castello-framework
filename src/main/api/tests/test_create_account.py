from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest


class TestCreateAccount:

    def test_create_account(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            db_session: Session
    ):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0, "Баланс нового счета должен быть нулевым"

        account_from_db = AccountCrudDb.get_required_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, "Аккаунт не создался, id аккаунта нет в БД"

    def test_create_more_than_two_accounts(
            self,
            api_manager: ApiManager,
            account_with_two_accounts: CreateUserRequest
    ):
        api_manager.user_steps.create_invalid_account(account_with_two_accounts)
