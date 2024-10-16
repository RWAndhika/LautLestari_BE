from models.base import Base

from sqlalchemy import Integer, String, DateTime, ForeignKey, LargeBinary, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship

class Products(Base):
    __tablename__ = 'products'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    image = mapped_column(String(255), nullable=False)
    price = mapped_column(Integer, nullable=False)
    qty = mapped_column(Integer, nullable=False)
    description = mapped_column(Text)
    category = mapped_column(String(255), nullable=False)
    location = mapped_column(String(255), nullable=False)
    nationality = mapped_column(String(255), nullable=False)
    size = mapped_column(Integer, nullable=False)
    referral_code = mapped_column(String(10))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    users = relationship('Users', back_populates='products')