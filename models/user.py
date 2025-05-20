from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  
    role = Column(String(50), default="user")  # Роль по умолчанию - "user"
    phone_number = Column(String(20), nullable=True)

    # Связь с заказами
    orders = relationship("Order", back_populates="user")
