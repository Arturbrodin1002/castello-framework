from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_last_transaction_by_type(
            db: Session,
            transaction_type: str,
            to_account_id: int | None = None,
            from_account_id: int | None = None,
            credit_id: int | None = None
    ) -> Transaction | None:
        query = db.query(Transaction).filter_by(transaction_type=transaction_type)

        if to_account_id is not None:
            query = query.filter_by(to_account_id=to_account_id)
        if from_account_id is not None:
            query = query.filter_by(from_account_id=from_account_id)
        if credit_id is not None:
            query = query.filter_by(credit_id=credit_id)

        return query.order_by(Transaction.id.desc()).first()

    @staticmethod
    def get_required_last_transaction_by_type(
            db: Session,
            transaction_type: str,
            to_account_id: int | None = None,
            from_account_id: int | None = None,
            credit_id: int | None = None
    ) -> Transaction:
        transaction = TransactionCrudDb.get_last_transaction_by_type(
            db=db,
            transaction_type=transaction_type,
            to_account_id=to_account_id,
            from_account_id=from_account_id,
            credit_id=credit_id
        )
        assert transaction is not None, f"Транзакция типа {transaction_type} не найдена в БД"
        return transaction
