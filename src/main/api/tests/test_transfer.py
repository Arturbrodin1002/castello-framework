from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest


class TestTransfer:
    def test_transfer_valid(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_response: CreateAccountResponse,
            second_account_response: CreateAccountResponse,
            db_session: Session
    ):
        api_manager.user_steps.deposit(
            create_user_request,
            DepositRequest(accountId=account_response.id, amount=1000)
        )
        transfer_request = TransferRequest(
            fromAccountId=account_response.id,
            toAccountId=second_account_response.id,
            amount=500
        )
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert response.fromAccountId == account_response.id
        assert response.toAccountId == second_account_response.id
        assert response.fromAccountIdBalance == 500

        sender_account_from_db = AccountCrudDb.get_account_by_id(db_session, account_response.id)
        receiver_account_from_db = AccountCrudDb.get_account_by_id(db_session, second_account_response.id)
        assert sender_account_from_db.balance == 500
        assert receiver_account_from_db.balance == 500

        transaction_from_db = TransactionCrudDb.get_last_transaction_by_type(
            db_session,
            transaction_type="transfer",
            to_account_id=second_account_response.id,
            from_account_id=account_response.id
        )
        assert transaction_from_db is not None, "Транзакция перевода не записалась в БД"
        assert transaction_from_db.amount == 500

    def test_transaction_history_after_transfer(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_response: CreateAccountResponse,
            second_user_request: CreateUserRequest,
            second_account_response: CreateAccountResponse
    ):
        api_manager.user_steps.deposit(
            create_user_request,
            DepositRequest(accountId=account_response.id, amount=1000)
        )
        api_manager.user_steps.transfer(
            create_user_request,
            TransferRequest(
                fromAccountId=account_response.id,
                toAccountId=second_account_response.id,
                amount=500
            )
        )

        sender_history = api_manager.user_steps.get_account_transactions(create_user_request, account_response.id)
        receiver_history = api_manager.user_steps.get_account_transactions(second_user_request, second_account_response.id)

        assert any(transaction["type"] == "deposit" for transaction in sender_history["transactions"])
        assert any(transaction["type"] == "transfer_out" for transaction in sender_history["transactions"])
        assert any(transaction["type"] == "transfer_in" for transaction in receiver_history["transactions"])

    def test_transfer_without_money(
            self,
            api_manager: ApiManager,
            create_user_request: CreateUserRequest,
            account_response: CreateAccountResponse,
            second_account_response: CreateAccountResponse,
            db_session: Session
    ):
        transfer_request = TransferRequest(
            fromAccountId=account_response.id,
            toAccountId=second_account_response.id,
            amount=500
        )
        api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        sender_account_from_db = AccountCrudDb.get_account_by_id(db_session, account_response.id)
        receiver_account_from_db = AccountCrudDb.get_account_by_id(db_session, second_account_response.id)
        assert sender_account_from_db.balance == 0
        assert receiver_account_from_db.balance == 0
