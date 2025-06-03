from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    bookings = relationship('Booking', back_populates='client', cascade='all, delete-orphan')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return name

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        return email

    @classmethod
    def create(cls, session, name, email):
        client = cls(name=name, email=email)
        session.add(client)
        session.commit()
        return client

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, client_id):
        return session.query(cls).get(client_id)

    @classmethod
    def delete(cls, session, client_id):
        client = cls.find_by_id(session, client_id)
        if client:
            session.delete(client)
            session.commit()
            return True
        return False

    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name}, email={self.email})>"

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

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    seat_number = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    bus_id = Column(Integer, ForeignKey('buses.id'), nullable=False)
    client = relationship('Client', back_populates='bookings')
    bus = relationship('Bus', back_populates='bookings')

    def __init__(self, seat_number, client, bus):
        self.seat_number = seat_number
        self.client = client
        self.bus = bus

    @validates('seat_number')
    def validate_seat_number(self, key, seat):
        if not isinstance(seat, int) or seat <= 0:
            raise ValueError("Seat number must be a positive integer")
        if self.bus and (seat > self.bus.capacity):
            raise ValueError(f"Seat number must be between 1 and {self.bus.capacity}")
        return seat

    @classmethod
    def create(cls, session, seat_number, client, bus):
        if session.query(cls).filter_by(bus_id=bus.id, seat_number=seat_number).first():
            raise ValueError("Seat already booked")
        booking = cls(seat_number=seat_number, client=client, bus=bus)
        session.add(booking)
        session.commit()
        return booking

    @classmethod
    def delete(cls, session, booking_id):
        booking = session.query(cls).get(booking_id)
        if booking:
            session.delete(booking)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, booking_id):
        return session.query(cls).get(booking_id)

    def __repr__(self):
        return f"<Booking(id={self.id}, seat={self.seat_number}, client_id={self.client_id}, bus_id={self.bus_id})>"