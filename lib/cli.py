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

@cli.command()
@click.argument('booking_id', type=int)
def find_booking(booking_id):
    """Find a booking by BOOKING_ID"""
    session = setup_database()
    booking = Booking.find_by_id(session, booking_id)
    if booking:
        click.echo(f"Booking ID: {booking.id}, Passenger: {booking.passenger_name}, Seat: {booking.seat_number}, Bus ID: {booking.bus_id}")
    else:
        click.echo(f"Error: Booking with ID {booking_id} not found")

def main_menu():
    while True:
        click.clear()
        click.echo("Bus Booking System")
        click.echo("1. Add Bus")
        click.echo("2. Add Booking")
        click.echo("3. List Buses")
        click.echo("4. List Bookings")
        click.echo("5. Delete Bus")
        click.echo("6. Delete Booking")
        click.echo("7. Find Bus")
        click.echo("8. Find Booking")
        click.echo("9. Exit")
        choice = click.prompt("Select an option (1-9)", type=int)
        
        if choice == 1:
            route = click.prompt("Enter route")
            capacity = click.prompt("Enter capacity", type=int)
            add_bus(route, capacity)
        elif choice == 2:
            bus_id = click.prompt("Enter bus ID", type=int)
            passenger_name = click.prompt("Enter passenger name")
            seat_number = click.prompt("Enter seat number", type=int)
            add_booking(bus_id, passenger_name, seat_number)
        elif choice == 3:
            list_buses()
        elif choice == 4:
            bus_id = click.prompt("Enter bus ID", type=int)
            list_bookings(bus_id)
        elif choice == 5:
            bus_id = click.prompt("Enter bus ID", type=int)
            delete_bus(bus_id)
        elif choice == 6:
            booking_id = click.prompt("Enter booking ID", type=int)
            delete_booking(booking_id)
        elif choice == 7:
            bus_id = click.prompt("Enter bus ID", type=int)
            find_bus(bus_id)
        elif choice == 8:
            booking_id = click.prompt("Enter booking ID", type=int)
            find_booking(booking_id)
        elif choice == 9:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid option. Please select 1-9.")
        click.pause()

if __name__ == '__main__':
    main_menu()