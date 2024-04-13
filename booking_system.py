import random
import string

class SeatBookingSystem:
    def __init__(self):
        self.seating = {row: ['A'] * 80 for row in 'ABCDEF'}
        self.booked_seats = {}  # Store seat details including booking reference
        self.references = set()  # Keep track of all issued booking references
        self.running = True  # Control the running of the menu

    def generate_unique_reference(self):
        """Generate a unique alphanumeric booking reference of exactly eight characters.
        The function ensures that each reference is unique by comparing against a set of previously generated references.
        """
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if reference not in self.references:
                self.references.add(reference)
                return reference

    def display_menu(self):
        # Display the menu options to the user
        print("\nSeat Booking System")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking state")
        print("5. Exit program")
        self.menu_selection()

    def menu_selection(self):
        # Take input from the user for menu selection
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            self.check_availability()
        elif choice == '2':
            self.book_seat()
        elif choice == '3':
            self.free_seat()
        elif choice == '4':
            self.show_booking_state()
        elif choice == '5':
            self.exit_program()
        else:
            print("Invalid choice. Please select from 1 to 5.")

    def check_availability(self):
        # Check if a particular seat is available
        seat = input("Enter the seat number (e.g., 1A): ").upper()
        row, number = seat[0], int(seat[1:])
        if row in self.seating and self.seating[row][number - 1] == 'A':
            print(f"Seat {seat} is available.")
        else:
            print(f"Seat {seat} is not available or does not exist.")

    def book_seat(self):
        seat = input("Enter the seat number to book (e.g., B5): ").upper()
        row, number = seat[0], int(seat[1:]) - 1
        if self.seating[row][number] == 'A':
            reference = self.generate_unique_reference()
            self.seating[row][number] = reference
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            passport_number = input("Enter passport number: ")
            # Store booking details
            self.booked_seats[reference] = {
                'passport_number': passport_number,
                'first_name': first_name,
                'last_name': last_name,
                'seat': f"{row}{number + 1}"
            }
            print(f"Seat {seat} has been successfully booked with reference {reference}.")
        else:
            print(f"Seat {seat} cannot be booked.")

    def free_seat(self):
        seat = input("Enter the seat number to free (e.g., B5): ").upper()
        row, number = seat[0], int(seat[1:]) - 1
        reference = self.seating[row][number]
        if isinstance(reference, str) and len(reference) == 8:
            self.seating[row][number] = 'F'
            del self.booked_seats[reference]
            print(f"Seat {seat} has been successfully freed.")
        else:
            print(f"Seat {seat} is not currently booked or does not exist.")

    def show_booking_state(self):
        # ANSI color codes for terminal output
        GREEN = '\033[92m'
        RED = '\033[91m'
        RESET = '\033[0m'

        print("\nBooking State:")
        for row in self.seating:
            row_display = f"Row {row}: "
            for seat_number in range(1, 81):
                seat_status = self.seating[row][seat_number - 1]
                color = GREEN if seat_status == 'A' else RED
                row_display += f"{row}{seat_number} {color}{seat_status}{RESET} "
            print(row_display.strip())

    def exit_program(self):
        # Exit the program
        self.running = False
        print("Exiting the program.")


# Create an instance of the booking system and start the menu
booking_system = SeatBookingSystem()
while booking_system.running:
    booking_system.display_menu()
