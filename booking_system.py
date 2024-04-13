import json
import random
import string
import os
from tabulate import tabulate
from colorama import init, Fore, Style


class SeatBookingSystem:
    ROWS = 'ABCDEF'  # Rows in the plane
    SEATS_PER_ROW = 80  # Number of seats per row
    DATA_FILE = "booked_seats.json"  # File to store booking data

    def __init__(self):
        self.load_data()

    def load_data(self):
        """Load booking data from the JSON file."""
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'r') as file:
                data = json.load(file)
                self.booked_seats = data.get('booked_seats', {})
                self.references = set(data.get('references', []))
                # Initialize seating arrangement with available seats
                self.seating = {row: ['A'] * self.SEATS_PER_ROW for row in self.ROWS}
                # Update seating arrangement with booked seats
                for ref, details in self.booked_seats.items():
                    row, column = details['seat_row'], details['seat_column']
                    self.seating[row][column - 1] = ref
        else:
            # Create a new JSON file with default values if it doesn't exist
            self.save_data()

    def generate_unique_reference(self):
        """Generate a unique booking reference."""
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if reference not in self.references:
                self.references.add(reference)
                return reference

    def save_data(self):
        """Save booking data to the JSON file."""
        data = {
            'booked_seats': self.booked_seats,
            'references': list(self.references)
        }
        with open(self.DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    def display_menu(self):
        """Display the menu options."""
        print("\nSeat Booking System")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking state")
        print("5. Display seating arrangement")
        print("6. Exit program")
        self.menu_selection()

    def menu_selection(self):
        """Handle user menu selection."""
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            self.check_availability()
        elif choice == '2':
            self.book_seat()
        elif choice == '3':
            self.free_seat()
        elif choice == '4':
            self.show_booking_state()
        elif choice == '5':
            self.display_seating_arrangement()
        elif choice == '6':
            self.exit_program()
        else:
            print("Invalid choice. Please select from 1 to 6.")

    def check_availability(self):
        """Check the availability of a seat."""
        seat = input("Enter the seat number (e.g., B5): ").upper()
        row, number = seat[0], int(seat[1:]) - 1
        if row not in self.seating or not (0 <= number < self.SEATS_PER_ROW):
            print("Invalid seat number. Please enter a valid seat number.")
            return
        if self.seating[row][number] == 'A':
            print(f"Seat {seat} is available.")
        else:
            print(f"Seat {seat} is not available or does not exist.")

    def book_seat(self):
        """Book a seat."""
        seat = input("Enter the seat number to book (e.g., B5): ").upper()
        row, number = seat[0], int(seat[1:]) - 1
        if row not in self.ROWS:
            print("Invalid seat number. Please enter a valid seat number.")
            return
        if not (0 <= number < self.SEATS_PER_ROW):
            print(f"Seat number {number + 1} is out of range for row {row}.")
            return
        if self.seating.get(row) and self.seating[row][number] == 'A':
            reference = self.generate_unique_reference()
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            passport_number = input("Enter passport number: ")
            self.seating[row][number] = reference
            self.booked_seats[reference] = {
                'passport_number': passport_number,
                'first_name': first_name,
                'last_name': last_name,
                'seat_row': row,
                'seat_column': number + 1
            }
            self.save_data()
            self.load_data()  # Reload data after modification
            print(f"Seat {seat} has been successfully booked with reference {reference}.")
        else:
            print(f"Seat {seat} cannot be booked.")

    def free_seat(self):
        """Free a booked seat."""
        reference = input("Enter the booking reference to free (e.g., FG6F8GOE): ").upper()
        if reference in self.booked_seats:
            seat_row = self.booked_seats[reference]['seat_row']
            seat_column = self.booked_seats[reference]['seat_column'] - 1
            self.seating[seat_row][seat_column] = 'A'
            del self.booked_seats[reference]
            self.references.remove(reference)
            self.save_data()
            self.load_data()  # Reload data after modification
            print(f"Seat booked with reference {reference} has been successfully freed.")
        else:
            print(f"Booking with reference {reference} does not exist.")

    def show_booking_state(self):
        """Display the booking state."""
        data_to_display = [
            [ref, details['first_name'], details['last_name'], details['passport_number'], details['seat_row'], details['seat_column']]
            for ref, details in self.booked_seats.items()
        ]
        headers = ["Booking Ref", "First Name", "Last Name", "Passport Number", "Row", "Column"]
        print(tabulate(data_to_display, headers=headers, tablefmt='grid'))

    def display_seating_arrangement(self):
        """Display the seating arrangement."""
        print("\nSeating Arrangement:")
        headers = ["Seat"] + [str(i) for i in range(1, self.SEATS_PER_ROW + 1)]
        data_to_display = []
        for row, seats in self.seating.items():
            row_data = [row]
            for seat_status in seats:
                if seat_status == 'A':
                    seat_display = Fore.GREEN + "■" + Style.RESET_ALL  # Green block for available seat
                else:
                    seat_display = Fore.RED + "■" + Style.RESET_ALL  # Red block for booked seat
                row_data.append(seat_display)
            data_to_display.append(row_data)
        print(tabulate(data_to_display, headers=headers, tablefmt='grid'))

    @staticmethod
    def exit_program():
        """Exit the program."""
        print("Exiting the program.")
        exit()


init()  # Initialize colorama

# Create an instance of the booking system and start the menu
booking_system = SeatBookingSystem()
while True:
    booking_system.display_menu()
