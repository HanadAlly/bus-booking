import click
from sqlalchemy.orm import exc
from models import Bus, Booking
from db_config import setup_database

@click.group()
def cli():
    """Bus Booking System CLI"""
    pass

@cli.command()
@click.argument('route')
@click.argument('capacity', type=int)
def add_bus(route, capacity):
    """Add a new bus with ROUTE and CAPACITY"""
    session = setup_database()
    try:
        bus = Bus.create(session, route, capacity)
        click.echo(f"Added bus: ID {bus.id}, Route {bus.route}, Capacity {bus.capacity}")
    except ValueError as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument('bus_id', type=int)
@click.argument('passenger_name')
@click.argument('seat_number', type=int)
def add_booking(bus_id, passenger_name, seat_number):
    """Add a booking for BUS_ID with PASSENGER_NAME and SEAT_NUMBER"""
    session = setup_database()
    try:
        bus = Bus.find_by_id(session, bus_id)
        if not bus:
            click.echo(f"Error: Bus with ID {bus_id} not found")
            return
        booking = Booking.create(session, passenger_name, seat_number, bus)
        click.echo(f"Booking added: ID {booking.id}, {passenger_name} on bus {bus_id}, seat {seat_number}")
    except ValueError as e:
        click.echo(f"Error: {e}")

