import gspread  # to manage Google sheets
from google.oauth2.service_account import Credentials
import sys  # used typing effect
import time  # for time operations
from tabulate import tabulate  # table prints
import os  # used for clearing terminal
import random  # random time and price
from datetime import datetime, timedelta  # time operations
import string  # for random reservation number


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


# Access to 'byron-air' google spreadsheet
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('byron-air')

LOGO = """

                            Welcome to ByronAir
                            
                                    |
                              --====|====--
                                    |
                                .-------.
                              .'_________'.
                             ._/_|__|__|_\_.
                            ;'-._       _.-';
       ,--------------------|    `-. .-'    |--------------------,
        ``----..__    ___   ;       '       ;   ___    __..----``
                  `"- / \ .._\             /_.. / \-"`
                      \_/    '._        _.'     \_/
                      `"`        ``---``        `"`

"""

LUGGAGE = """
                    ____
               .---[[__]]----.
              ;-------------.|       ____
              |             ||   .--[[__]]---.
              |             ||  ;-----------.|
              |             ||  |           ||
              |_____________|/  |           ||
                                |___________|/
"""


def welcome():
    """
    Print logo.
    """
    print(f"\033[33m{LOGO}\033[0m")


# Dictionary will contain all booking info and upload it to the spreadsheet
booking = {
    'Departure': '',
    'Arrival': '',
    'Departure Date': '',
    'Main Passenger Name': '',
    'Total Number of Passengers': '',
    'Time of Departure': '',
    'Time of Arrival': '',
    'Check-in Bags': '',
    'Price': '',
    "Reservation Number": ''
}


def typing_print(text, delay=0.02):
    """
    Typing effect to print statements
    """
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)


def typing_input(text, delay=0.02):
    """
    Typing effect to inputs
    """
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
    value = input()
    return value


def clear_terminal():
    """
    function to clear terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    """
    Function displays main menu with option to
    make a booking or retrieve booking
    """
    clear_terminal()
    welcome()

    menu = [
        ["\033[32m1", "Make a Booking\033[0m"],
        ["\033[34m2", "Retrieve Booking\033[0m"]
    ]

    typing_print(tabulate(menu))
    while True:
        try:
            option = int(
                typing_input("\nPress \033[32m1\033[0m to Make a Booking or \
\033[34m2\033[0m to Retrieve your Booking:\n"))

            if option == 1:
                clear_terminal()
                make_a_booking()
                break

            elif option == 2:
                clear_terminal()
                pull_reservation_details()
                break

            else:
                print("\033[31mInvalid option, please try again.\033[0m\n")
        except ValueError:
            print("\033[31mInvalid option, please try again.\033[0m\n")


def select_airport(direction, locked=None):
    """
    function will pull list of Countries from spreedsheet
    worksheets and depending on choice will print list of
    airports in that country
    """
    global booking
    clear_terminal()

    while True:
        try:
            # Iterate through worksheet titles skiping the first one
            sheet_names = [s.title for s in SHEET.worksheets()[1:]]
            for index, item in enumerate(sheet_names):
                # add 1 to the index as first worksheet is skipped.
                print(f"\033[32m{index + 1}\033[0m {item.title()}")
            print("\n")
            selection = int(
                typing_input(f"Please enter Country of {direction.capitalize()}:\n"))
            clear_terminal()
            # Get the airports for the selected country from the worksheet
            if sheet_names[selection - 1]:
                chosen_country_airports = SHEET.worksheet(
                    sheet_names[selection - 1]).get_all_values()[1:]

                # Print all airports included in selected Country.
                for airport in chosen_country_airports:
                    print(f"\033[32m{airport[0]}\033[0m {airport[1]}")
                chosen_airport = int(
                    typing_input(f"\nPlease choose your Airport of {direction.capitalize()}:\n"))
                # Remove 1 from chosen airport to connect it to worksheet.
                airport_to_add = chosen_country_airports[chosen_airport - 1][1]
                booking[direction] = airport_to_add

                # validations to check if both attributes are not the same.
                if (locked):
                    if (locked == airport_to_add):
                        print(
                            f"\033[31mArrival must be different than Departure.\033[0m\n")
                        return select_airport(direction, locked)

                return airport_to_add

            else:
                print("\033[31mPlease select correct Airport.\033[0m\n")
        except ValueError:
            print("\033[31mPlease enter correct Airport.\033[0m\n")
            clear_terminal()
        except IndexError:
            print("\033[31mPlease enter correct Value.\033[0m\n")
            clear_terminal()


def date_of_departure():
    """
    Function enable user to set date of departure.
    Date must be in the future and error is being
    handled by except ValueError
    """
    clear_terminal()
    print(f"Departure: \033[36m{booking['Departure'].upper()}\033[0m\n")
    print(f"Arrival: \033[35m{booking['Arrival'].upper()}\033[0m\n")
    while True:
        try:
            date_component = typing_input(
                "Please Enter departure date in DD/MM/YYYY format:\n")
            dep_date = datetime.strptime(date_component, "%d/%m/%Y").date()
            current_date = datetime.now().date()

            # Check to make sure that users date is in the future.
            if dep_date < current_date:
                print("\033[31mPlease provide date in the future.\033[0m\n")
                continue

            booking['Departure Date'] = dep_date.strftime('%d/%B/%Y')
            clear_terminal()
            choose_flight()
            break

        except ValueError:
            print("\033[31mPlease provide date in DD/MM/YYYY format\033[0m\n")


def generate_random_time(start_time_str, end_time_str, hours_to_add):
    """
    Function generates random time for departure and random time for arrival
    within chosen range. Arrival time with additional 2 hours added.
    """
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    # Calculate time range in minutes
    time_range = (end_time.hour - start_time.hour) * 60 + \
        (end_time.minute - start_time.minute)
    # Generate random number of minutes within range
    random_minutes = random.randint(0, time_range)
    # Combine the random minutes with start time and add additional hours
    random_time = datetime.combine(
        datetime.today(), start_time) + timedelta(minutes=random_minutes)
    # Add set extra hours to randomly generated time
    random_time += timedelta(hours=hours_to_add)
    return random_time.strftime("%H:%M")


# Random times depending on chosen flight
early = generate_random_time('06:00', '08:00', hours_to_add=0)
early_arr = generate_random_time("08:00", "10:00", hours_to_add=2)
midday = generate_random_time("14:00", "16:00", hours_to_add=0)
midday_arr = generate_random_time(
    "16:00", "18:00", hours_to_add=2)
late = generate_random_time("18:00", "20:00", hours_to_add=0)
late_arr = generate_random_time("20:00", "22:00", hours_to_add=2)


def generate_flight_price(min, max):
    """
    Function generates random price for the ticket
    """
    random_price = random.uniform(min, max)
    return random_price


# Different random prices depending on the chosen flight.
CURRENCY_SYMBOL = "€"
price_1 = generate_flight_price(100, 200)
price_2 = generate_flight_price(100, 200)
price_3 = generate_flight_price(100, 200)


def format_currency(value, currency_symbol):
    """
    Print flight price with currency attached
    """
    amount = f"{CURRENCY_SYMBOL}{value:.2f}"

    return amount


def choose_flight():
    """
    Function enables user to choose 1 out of 3 randomly generated flights.
    Departure and arrival has already been selected before.
    Time and price is being generated randomly."""
    global booking

    # List of available flights for user to choose from
    choose = [
        ["Num", "Departure", "Dep Time",
            "Arr Time", "Arrival", "Price"],
        ["\033[32m1\033[0m",
            f"\033[36m{booking['Departure']}\033[0m",
            early,
            early_arr,
            f"\033[35m{booking['Arrival']}\033[0m",
            format_currency(price_1, CURRENCY_SYMBOL)],
        ["\033[32m2\033[0m",
            f"\033[36m{booking['Departure']}\033[0m",
            midday,
            midday_arr,
            f"\033[35m{booking['Arrival']}\033[0m",
            format_currency(price_2, CURRENCY_SYMBOL)],
        ["\033[32m3\033[0m",
            f"\033[36m{booking['Departure']}\033[0m",
            late,
            late_arr,
            f"\033[35m{booking['Arrival']}\033[0m",
            format_currency(price_3, CURRENCY_SYMBOL)]]
    print(tabulate(choose, headers='firstrow', tablefmt='fancy_grid'))
    while True:
        try:
            flight = int(typing_input("Please choose an available flight:\n"))

            if flight in (1, 2, 3):
                booking["Time of Departure"] = [early, midday, late][flight-1]
                booking["Time of Arrival"] = [early_arr,
                                              midday_arr,
                                              late_arr][flight-1]
                booking["Price"] = [price_1, price_2, price_3][flight-1]
                passenger_name()
                break

            else:
                print("\033[31mPlease choose a correct flight..\033[0m\n")

        except ValueError:
            print("\033[31mPlease choose a correct flight..\033[0m\n")


def passenger_name():
    """
    Function have to input main passenger name that must
    contain at least first and last name. Both parts of the name
    are being capitalized by title()
    """
    clear_terminal()
    while True:
        try:
            name = input(
                "Please enter First and Last Name of Main Passenger:\n")
            parts = name.split()

            # Check if Name contains to parts.
            if len(parts) < 2:
                print(f"\033[31mPlease provide Full Name\033[0m")
                continue

            # Check if there are no digits in Name.
            if any(element.isdigit() for element in name):
                print("\033[31mName should not contain numbers\033[0m\n")
                continue

            else:
                # Remove all additional whitespaces and add to booking
                first_name = parts[0].capitalize()
                last_name = parts[1].capitalize()
                full_name = ' '.join([first_name, last_name])
                booking["Main Passenger Name"] = full_name
                total_amount_of_pax()
                break

        except ValueError:
            print("\033[31mName should not contain numbers\033[0m\n")


def total_amount_of_pax():
    """
    function add total amount of passengers to
    booking dictionary
    """
    while True:
        try:
            print("\n\033[33mMaximum number of Passengers is 10\033[0m")
            pax_amount = int(
                input("\nPlease provide Total amount of Passengers:\n"))

            # Validate correct number of passengers
            if pax_amount > 10:
                print(
                    "\033[31mTotal amount of Passenger cannot exceed 10\033[0m\n")
                continue

            else:
                booking["Total Number of Passengers"] = pax_amount
                price = booking["Price"]
                total_price = pax_amount * price
                booking["Price"] = total_price
                checked_in_bags()
                break

        except ValueError:
            print("\033[31mTotal amount of Passengers cannot exceed 10\033[0m\n")


def checked_in_bags():
    """
    function enables user to add amount of checked-in bags.
    Each bag costs 25 and user can only choose max 3 bags
    per passenger
    """
    bag_price = 25
    clear_terminal()
    print(LUGGAGE)
    while True:
        try:
            print("\n")
            print("There are \033[33m3\033[0m Bags allowed per passenger.\n")
            print("\033[33mPlease be aware that each Bag costs 25€:\033[0m\n")
            number_of_bags = int(input("Please provide amount of Bags:\n"))

            # Check to calculate correct number of bags allowed.
            booking["Check-in Bags"] = number_of_bags
            total_pax = booking["Total Number of Passengers"]
            max_bags = int(total_pax) * 3

            if number_of_bags > max_bags:
                print(
                    "\033[31mAmount of Bags cannot exceed 3 per Person.\033[0m\n")
                continue

            calculated_amount = int(
                booking["Price"]) + (number_of_bags * bag_price)
            booking["Price"] = calculated_amount
            reservation_number()
            reservation_details()
            break

        except ValueError:
            print("\033[31mPlease enter valid number of Bags.\033[0m\n")


def reservation_number():
    """
    function creates random 6 characters long reservation
    number that contains digits and letters.
    """
    r_number = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=6))
    booking["Reservation Number"] = r_number.upper()


def reservation_details():
    """
    function print details of the reservation.
    After pressing any key user is being brought back
    to the main menu.
    """
    clear_terminal()
    typing_print(
        f"Reservation: \033[33m{booking['Reservation Number']}:\033[0m\n")
    add_booking_row(booking)

    # Add CURRENCY SYMBOL to reservation print.
    booking['Price'] = f"{CURRENCY_SYMBOL}{booking['Price']}"
    booking_table = [[key, f"\033[36m{value}\033[0m"]
                     for key, value in booking.items()]

    print(tabulate(booking_table, tablefmt='grid'))
    typing_input("\nPlease press any key to go back to Main Menu..")
    main_menu()


def add_booking_row(booking):
    """
    Function adds all reservation details to the worksheet
    'bookings' appending new row each reservation.
    """
    worksheet = SHEET.worksheet('bookings')
    row_values = [
        booking['Departure'],
        booking['Arrival'],
        booking['Departure Date'],
        booking['Main Passenger Name'],
        booking['Total Number of Passengers'],
        booking['Time of Departure'],
        booking['Time of Arrival'],
        booking['Check-in Bags'],
        booking['Price'],
        booking['Reservation Number']
    ]
    worksheet.append_row(row_values)


def pull_reservation_details():
    """
    Function enables the user to input the reservation number
    of a previously created booking
    and view all the details of the booking.
    """
    booking_sheet = SHEET.worksheet('bookings')
    number = typing_input("Please enter your Reservation Number:\n")
    number = number.upper()
    # Read reservation number from the last column
    booking_numbers = booking_sheet.col_values(10)[1:]

    if number in booking_numbers:
        # Get row index of the reservation number
        row_index = booking_numbers.index(number) + 2
        # Retrieve all values from correct row
        booking_values = booking_sheet.row_values(row_index)
        headers = booking_sheet.row_values(1)
        # Creates dict with headers as keys and rows as values.
        booking_details = dict(zip(headers, booking_values))
        # Add currency symbol to printed price
        if 'Price' in booking_details:
            booking_details['Price'] = f"{CURRENCY_SYMBOL}{booking_details['Price']}"
        booking_print = [[key, f"\033[36m{value}\033[0m"]
                         for key, value in booking_details.items()]

        typing_print(
            f"Please see details of Reservation: \033[33m{number}\033[0m\n")
        print(tabulate(booking_print, tablefmt='grid'))
        typing_input("Press any key to go back to Main Menu")
        main_menu()

    else:
        print("\033[31mReservation Number not found.\033[0m")
        pull_reservation_details()


def make_a_booking():
    """
    function starts select_airport function
    to make sure that user first pick departure
    airport and then arrival airport.
    """
    dep_airport = select_airport("Departure")
    arr_airport = select_airport("Arrival", dep_airport)
    date_of_departure()


def main():
    """
    Start running functions
    """
    main_menu()


main()
