from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import OpenTickets, Base

engine = create_engine('sqlite:///db/database.db', echo=True)
Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

Base.metadata.create_all(engine)

def get_db():
    return Session()