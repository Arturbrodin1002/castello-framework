from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from src.main.api.db.models.base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    to_account_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    from_account_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    credit_id = Column(Integer, ForeignKey("credit.id"), nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, type={self.transaction_type}, "
            f"amount={self.amount})>"
        )
