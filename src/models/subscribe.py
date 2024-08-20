from models.base import Base

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

class Subscribe(Base):
    __tablename__ = 'subscribe'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(255), unique=True, nullable=False)
    