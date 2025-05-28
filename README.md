# Bus Booking System

## Description
A Python CLI application for managing bus routes and passenger bookings, built with SQLAlchemy for ORM and Click for the command-line interface. The application implements a one-to-many relationship between buses and bookings, allowing users to create, view, and delete buses and bookings with input validation.

## Setup
1. Clone the repository or create the project structure.
2. Install Pipenv: `pip install pipenv`
3. Install dependencies: `pipenv install`
4. Activate virtual environment: `pipenv shell`
5. Run the CLI: `python3 lib/cli.py`

## Usage
Run `python3 lib/cli.py` in the virtual environment to access the interactive menu. Available options:
- Add a bus: Create a new bus with a route and capacity.
- Add a booking: Book a seat for a passenger on a specific bus.
- List buses: Display all buses.
- List bookings: Show all bookings for a specific bus.
- Delete bus: Remove a bus and its associated bookings.
- Delete booking: Remove a specific booking.
- Find bus: Display details of a bus by ID.
- Find booking: Display details of a booking by ID.
- Exit: Close the application.

## Requirements
- Python 3.8+
- SQLite
- Pipenv