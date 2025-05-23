from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Добавляем связь с пользователем
    items = Column(JSON, nullable=False)  # Формат: [{"product_id": "mongo_id", "quantity": N}, ...]
    status = Column(String(20), default='new')
    created_at = Column(DateTime, default=datetime.utcnow)
    phone = Column(String(20))
    address = Column(String(255))

    # Определяем связь с моделью User
    user = relationship("User", back_populates="orders")

