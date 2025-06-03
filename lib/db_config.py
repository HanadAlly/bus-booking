from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def setup_database():
    """Setup the database and return a session"""
    engine = create_engine('sqlite:///bus_booking.db', echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()