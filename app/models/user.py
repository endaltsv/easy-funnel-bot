from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    channel_id = Column(String, nullable=False)
    joined_at = Column(DateTime, default=func.now())
