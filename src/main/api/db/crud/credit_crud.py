from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:
    @staticmethod
    def get_credit_by_id(db: Session, credit_id: int) -> Credit | None:
        return db.query(Credit).filter_by(id=credit_id).first()

    @staticmethod
    def get_required_credit_by_id(db: Session, credit_id: int) -> Credit:
        credit = CreditCrudDb.get_credit_by_id(db, credit_id)
        assert credit is not None, f"Кредит с id={credit_id} не найден в БД"
        return credit

    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=account_id).first()

    @staticmethod
    def get_required_credit_by_account_id(db: Session, account_id: int) -> Credit:
        credit = CreditCrudDb.get_credit_by_account_id(db, account_id)
        assert credit is not None, f"Кредит для счета id={account_id} не найден в БД"
        return credit

    @staticmethod
    def count_credits_by_account_id(db: Session, account_id: int) -> int:
        return db.query(Credit).filter_by(account_id=account_id).count()
