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

@cli.command()
def list_buses():
    """List all buses"""
    session = setup_database()
    buses = Bus.get_all(session)
    if not buses:
        click.echo("No buses available")
        return
    for bus in buses:
        click.echo(f"Bus ID: {bus.id}, Route: {bus.route}, Capacity: {bus.capacity}")

@cli.command()
@click.argument('bus_id', type=int)
def list_bookings(bus_id):
    """List all bookings for BUS_ID"""
    session = setup_database()
    bus = Bus.find_by_id(session, bus_id)
    if not bus:
        click.echo(f"Error: Bus with ID {bus_id} not found")
        return
    bookings = bus.bookings
    if not bookings:
        click.echo(f"No bookings for bus {bus_id}")
        return
    for booking in bookings:
        click.echo(f"Booking ID: {booking.id}, Passenger: {booking.passenger_name}, Seat: {booking.seat_number}")

@cli.command()
@click.argument('bus_id', type=int)
def delete_bus(bus_id):
    """Delete a bus by BUS_ID"""
    session = setup_database()
    if Bus.delete(session, bus_id):
        click.echo(f"Deleted bus with ID {bus_id}")
    else:
        click.echo(f"Error: Bus with ID {bus_id} not found")

@cli.command()
@click.argument('booking_id', type=int)
def delete_booking(booking_id):
    """Delete a booking by BOOKING_ID"""
    session = setup_database()
    if Booking.delete(session, booking_id):
        click.echo(f"Deleted booking with ID {booking_id}")
    else:
        click.echo(f"Error: Booking with ID {booking_id} not found")

@cli.command()
@click.argument('bus_id', type=int)
def find_bus(bus_id):
    """Find a bus by BUS_ID"""
    session = setup_database()
    bus = Bus.find_by_id(session, bus_id)
    if bus:
        click.echo(f"Bus ID: {bus.id}, Route: {bus.route}, Capacity: {bus.capacity}")
    else:
        click.echo(f"Error: Bus with ID {bus_id} not found")

