from sqlalchemy import Column, String, Text
from app.core.database import Base

class Funnel(Base):
    __tablename__ = "funnels"

    channel_id = Column(String, primary_key=True)  # @username или numeric
    text = Column(Text, nullable=True)
    button_type = Column(String, nullable=True)
    button_text = Column(String, nullable=True)
    button_url = Column(String, nullable=True)
