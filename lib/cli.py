import click
from models import Client, Bus, Booking
from db_config import setup_database

@click.group()
def cli():
    """Bus Booking System CLI"""
    pass

def add_client(name, email):
    """Add a new client with NAME and EMAIL"""
    session = setup_database()
    try:
        client = Client.create(session, name, email)
        click.echo(f"Added client: ID {client.id}, Name {client.name}, Email {client.email}")
    except ValueError as e:
        click.echo(f"Error: {e}")

def add_bus(route, capacity):
    """Add a new bus with ROUTE and CAPACITY"""
    session = setup_database()
    try:
        bus = Bus.create(session, route, capacity)
        click.echo(f"Added bus: ID {bus.id}, Route {bus.route}, Capacity {bus.capacity}")
    except ValueError as e:
        click.echo(f"Error: {e}")

def add_booking(client_id, bus_id, seat_number):
    """Add a booking for CLIENT_ID on BUS_ID with SEAT_NUMBER"""
    session = setup_database()
    try:
        client = Client.find_by_id(session, client_id)
        if not client:
            click.echo(f"Error: Client with ID {client_id} not found")
            return
        bus = Bus.find_by_id(session, bus_id)
        if not bus:
            click.echo(f"Error: Bus with ID {bus_id} not found")
            return
        booking = Booking.create(session, seat_number, client, bus)
        click.echo(f"Booking added: ID {booking.id}, Client {client.name}, Bus {bus_id}, Seat {seat_number}")
    except ValueError as e:
        click.echo(f"Error: {e}")

def list_clients():
    """List all clients"""
    session = setup_database()
    clients = Client.get_all(session)
    if not clients:
        click.echo("No clients available")
        return
    for client in clients:
        click.echo(f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}")

def list_buses():
    """List all buses"""
    session = setup_database()
    buses = Bus.get_all(session)
    if not buses:
        click.echo("No buses available")
        return
    for bus in buses:
        click.echo(f"Bus ID: {bus.id}, Route: {bus.route}, Capacity: {bus.capacity}")

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
        click.echo(f"Booking ID: {booking.id}, Client: {booking.client.name}, Seat: {booking.seat_number}")

def delete_client(client_id):
    """Delete a client by CLIENT_ID"""
    session = setup_database()
    if Client.delete(session, client_id):
        click.echo(f"Deleted client with ID {client_id}")
    else:
        click.echo(f"Error: Client with ID {client_id} not found")

def delete_bus(bus_id):
    """Delete a bus by BUS_ID"""
    session = setup_database()
    if Bus.delete(session, bus_id):
        click.echo(f"Deleted bus with ID {bus_id}")
    else:
        click.echo(f"Error: Bus with ID {bus_id} not found")

def delete_booking(booking_id):
    """Delete a booking by BOOKING_ID"""
    session = setup_database()
    if Booking.delete(session, booking_id):
        click.echo(f"Deleted booking with ID {booking_id}")
    else:
        click.echo(f"Error: Booking with ID {booking_id} not found")

def find_client(client_id):
    """Find a client by CLIENT_ID"""
    session = setup_database()
    client = Client.find_by_id(session, client_id)
    if client:
        click.echo(f"Client ID: {client.id}, Name: {client.name}, Email: {client.email}")
    else:
        click.echo(f"Error: Client with ID {client_id} not found")

def find_bus(bus_id):
    """Find a bus by BUS_ID"""
    session = setup_database()
    bus = Bus.find_by_id(session, bus_id)
    if bus:
        click.echo(f"Bus ID: {bus.id}, Route: {bus.route}, Capacity: {bus.capacity}")
    else:
        click.echo(f"Error: Bus with ID {bus_id} not found")

def find_booking(booking_id):
    """Find a booking by BOOKING_ID"""
    session = setup_database()
    booking = Booking.find_by_id(session, booking_id)
    if booking:
        click.echo(f"Booking ID: {booking.id}, Client: {booking.client.name}, Seat: {booking.seat_number}, Bus ID: {booking.bus_id}")
    else:
        click.echo(f"Error: Booking with ID {booking_id} not found")

# Keep Click commands for direct CLI usage
@cli.command()
@click.argument('name')
@click.argument('email')
def add_client_cmd(name, email):
    """Add a new client via command line"""
    add_client(name, email)

@cli.command()
@click.argument('route')
@click.argument('capacity', type=int)
def add_bus_cmd(route, capacity):
    """Add a new bus via command line"""
    add_bus(route, capacity)

@cli.command()
@click.argument('client_id', type=int)
@click.argument('bus_id', type=int)
@click.argument('seat_number', type=int)
def add_booking_cmd(client_id, bus_id, seat_number):
    """Add a booking via command line"""
    add_booking(client_id, bus_id, seat_number)

@cli.command()
def list_clients_cmd():
    """List all clients via command line"""
    list_clients()

@cli.command()
def list_buses_cmd():
    """List all buses via command line"""
    list_buses()

@cli.command()
@click.argument('bus_id', type=int)
def list_bookings_cmd(bus_id):
    """List all bookings for BUS_ID via command line"""
    list_bookings(bus_id)

@cli.command()
@click.argument('client_id', type=int)
def delete_client_cmd(client_id):
    """Delete a client via command line"""
    delete_client(client_id)

@cli.command()
@click.argument('bus_id', type=int)
def delete_bus_cmd(bus_id):
    """Delete a bus via command line"""
    delete_bus(bus_id)

@cli.command()
@click.argument('booking_id', type=int)
def delete_booking_cmd(booking_id):
    """Delete a booking via command line"""
    delete_booking(booking_id)

@cli.command()
@click.argument('client_id', type=int)
def find_client_cmd(client_id):
    """Find a client via command line"""
    find_client(client_id)

@cli.command()
@click.argument('bus_id', type=int)
def find_bus_cmd(bus_id):
    """Find a bus via command line"""
    find_bus(bus_id)

@cli.command()
@click.argument('booking_id', type=int)
def find_booking_cmd(booking_id):
    """Find a booking via command line"""
    find_booking(booking_id)

def main_menu():
    # List for menu options
    menu_options = [
        "Add Client",
        "Add Bus",
        "Add Booking",
        "List Clients",
        "List Buses",
        "List Bookings",
        "Delete Client",
        "Delete Bus",
        "Delete Booking",
        "Find Client",
        "Find Bus",
        "Find Booking",
        "Exit"
    ]
    # Dictionary for validation rules
    validation_rules = {
        "name": ("Name must be at least 2 characters", lambda x: len(x.strip()) >= 2),
        "email": ("Invalid email format", lambda x: '@' in x and '.' in x),
        "route": ("Route must be at least 3 characters", lambda x: len(x.strip()) >= 3),
        "capacity": ("Capacity must be positive", lambda x: isinstance(x, int) and x > 0),
        "seat": ("Seat must be positive", lambda x: isinstance(x, int) and x > 0)
    }
    # Tuple for menu display
    menu_display = tuple(f"{i+1}. {option}" for i, option in enumerate(menu_options))

    while True:
        click.clear()
        click.echo("Bus Booking System")
        for option in menu_display[:-1]:
            click.echo(option)
        click.echo(menu_display[-1])  # Exit option
        choice = click.prompt("Select an option (1-13)", type=int)

        if choice == 1:
            name = click.prompt("Enter name")
            email = click.prompt("Enter email")
            add_client(name, email)
        elif choice == 2:
            route = click.prompt("Enter route")
            capacity = click.prompt("Enter capacity", type=int)
            add_bus(route, capacity)
        elif choice == 3:
            client_id = click.prompt("Enter client ID", type=int)
            bus_id = click.prompt("Enter bus ID", type=int)
            seat_number = click.prompt("Enter seat number", type=int)
            add_booking(client_id, bus_id, seat_number)
        elif choice == 4:
            list_clients()
        elif choice == 5:
            list_buses()
        elif choice == 6:
            bus_id = click.prompt("Enter bus ID", type=int)
            list_bookings(bus_id)
        elif choice == 7:
            client_id = click.prompt("Enter client ID", type=int)
            delete_client(client_id)
        elif choice == 8:
            bus_id = click.prompt("Enter bus ID", type=int)
            delete_bus(bus_id)
        elif choice == 9:
            booking_id = click.prompt("Enter booking ID", type=int)
            delete_booking(booking_id)
        elif choice == 10:
            client_id = click.prompt("Enter client ID", type=int)
            find_client(client_id)
        elif choice == 11:
            bus_id = click.prompt("Enter bus ID", type=int)
            find_bus(bus_id)
        elif choice == 12:
            booking_id = click.prompt("Enter booking ID", type=int)
            find_booking(booking_id)
        elif choice == 13:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid option. Please select 1-13.")
        click.pause()

if __name__ == '__main__':
    main_menu()