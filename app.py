class SeatBookingSystem:
    def __init__(self):
        # Initialize the seating with 6 rows (A-F) and 80 seats in each row (1-80)
        self.seating = {row: ['A'] * 80 for row in 'ABCDEF'}
        self.running = True  # Control the running of the menu

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
        # Book a seat if it is available
        seat = input("Enter the seat number to book (e.g., B5): ").upper()
        row, number = seat[0], seat[1:]  # Correctly parse the row and number
        try:
            number = int(number) - 1
            if row in self.seating and self.seating[row][number] == 'A':
                self.seating[row][number] = 'R'
                print(f"Seat {seat} has been successfully booked.")
            else:
                print(f"Seat {seat} cannot be booked or does not exist.")
        except ValueError:
            print("Invalid seat number. Please enter a valid seat such as B5.")

    def free_seat(self):
        # Free a booked seat
        seat = input("Enter the seat number to free (e.g., B5): ").upper()
        row, number = seat[0], seat[1:]  # Correctly parse the row and number
        try:
            number = int(number) - 1
            if row in self.seating and self.seating[row][number] == 'R':
                self.seating[row][number] = 'A'
                print(f"Seat {seat} has been successfully freed.")
            else:
                print(f"Seat {seat} is not currently booked or does not exist.")
        except ValueError:
            print("Invalid seat number. Please enter a valid seat such as B5.")

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
