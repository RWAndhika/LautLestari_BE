from models.base import Base

from sqlalchemy import Integer,  ForeignKey, String
from sqlalchemy.orm import mapped_column

class Carts(Base):
    __tablename__ = 'carts'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    product_id = mapped_column(Integer, ForeignKey('products.id'))
    qty = mapped_column(Integer, nullable=False)
    price = mapped_column(Integer, nullable=False)
    description = mapped_column(String(500), nullable=False)
    