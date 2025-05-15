from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from user import User

from db.session import Base

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)  # Статус заявки
    description = Column(String(255), nullable=True)  # Описание заявки
    created_at = Column(String(50), nullable=False)  # Дата создания заявки
    updated_at = Column(String(50), nullable=True)  # Дата обновления заявки
    products_ids = Column(JSON)
