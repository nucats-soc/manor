from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class OpenTickets(Base):
    __tablename__ = 'open_tickets'

    user_id = Column(Integer, unique=True, nullable=False)
    channel_id = Column(Integer, primary_key=True, nullable=False)