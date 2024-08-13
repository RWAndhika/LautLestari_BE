from models.base import Base

from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

class Confirmations(Base):
    __tablename__ = 'confirmations'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    buyer = mapped_column(String(255), nullable=False)
    products_id = mapped_column(Integer, ForeignKey('products.id'))
    price = mapped_column(Integer, nullable=False)
    qty = mapped_column(Integer, nullable=False)
    description = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_confirm = mapped_column(Integer, nullable=False)