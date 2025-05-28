from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()

class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True)
    route = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    bookings = relationship('Booking', back_populates='bus', cascade='all, delete-orphan')

    def __init__(self, route, capacity):
        self.route = route
        self.capacity = capacity

    @validates('route')
    def validate_route(self, key, route):
        if not route or len(route.strip()) < 3:
            raise ValueError("Route must be at least 3 characters long")
        return route

    @validates('capacity')
    def validate_capacity(self, key, capacity):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        return capacity

    @classmethod
    def create(cls, session, route, capacity):
        bus = cls(route=route, capacity=capacity)
        session.add(bus)
        session.commit()
        return bus

    @classmethod
    def delete(cls, session, bus_id):
        bus = session.query(cls).get(bus_id)
        if bus:
            session.delete(bus)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, bus_id):
        return session.query(cls).get(bus_id)

    def __repr__(self):
        return f"<Bus(id={self.id}, route={self.route}, capacity={self.capacity})>"
