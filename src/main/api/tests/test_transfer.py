from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest


class TestTransfer:
    def test_transfer_valid(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            transfer_request: TransferRequest,
            db_session: Session
    ):
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert response.fromAccountIdBalance == 500, "После перевода баланс отправителя в ответе должен стать 500"

        sender_account_from_db = AccountCrudDb.get_required_account_by_id(db_session, transfer_request.fromAccountId)
        receiver_account_from_db = AccountCrudDb.get_required_account_by_id(db_session, transfer_request.toAccountId)
        assert sender_account_from_db.balance == 500, "После перевода баланс отправителя в БД должен стать 500"
        assert receiver_account_from_db.balance == 500, "После перевода баланс получателя в БД должен стать 500"

    def test_transaction_history_after_transfer(
            self,
            transfer_history_response
    ):
        sender_history, receiver_history = transfer_history_response

        assert any(transaction["type"] == "deposit" for transaction in sender_history["transactions"]), "История отправителя не содержит deposit"
        assert any(transaction["type"] == "transfer_out" for transaction in sender_history["transactions"]), "История отправителя не содержит transfer_out"
        assert any(transaction["type"] == "transfer_in" for transaction in receiver_history["transactions"]), "История получателя не содержит transfer_in"

    def test_transfer_without_money(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            invalid_transfer_request: TransferRequest,
            db_session: Session
    ):
        api_manager.user_steps.transfer_invalid(create_user_request, invalid_transfer_request)

        sender_account_from_db = AccountCrudDb.get_required_account_by_id(db_session, invalid_transfer_request.fromAccountId)
        receiver_account_from_db = AccountCrudDb.get_required_account_by_id(db_session, invalid_transfer_request.toAccountId)
        assert sender_account_from_db.balance == 0, "При переводе без денег баланс отправителя должен остаться нулевым"
        assert receiver_account_from_db.balance == 0, "При переводе без денег баланс получателя должен остаться нулевым"
