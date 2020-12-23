import random
import sqlite3


class DatabaseManager:

    def __init__(self):
        self.db_name = "./card.s3db"
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as errorMsg:
            print(errorMsg)

    def setup_table(self):
        """Creates a table if it does not exist"""
        self.cursor.execute("DROP TABLE IF EXISTS card")
        self.conn.commit()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS card
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
          number TEXT,
          pin TEXT,
          balance INTEGER DEFAULT 0)""")
        self.conn.commit()

    def insert_new_data(self, a_number, a_pin):
        """Inserts a row into the table card"""
        # id_ = len(self.cursor.fetchall()) + 1
        data = (a_number, a_pin, 0)

        self.cursor.execute("INSERT INTO card (number, pin, balance) VALUES (?,?,?)", data)
        self.conn.commit()

    def get_balance(self, a_number, a_pin):
        """Gets the balance if"""
        data = (a_number, a_pin)
        balance = 0

        try:
            self.cursor.execute("SELECT balance FROM card WHERE number=? AND pin=?", data)
            balance = self.cursor.fetchone()
        except Exception as e:
            print("No such account.")
        return balance

    def display_all_data(self):
        for row in self.cursor.execute("SELECT * FROM card"):
            print(row)

    def close(self):
        self.cursor.close()
        self.conn.close()


# 16 digits long card number
# 1-6: IIN must be 400_000 (first six digits)
# 7-15: Account number: unique (9 digits)
# 16: Check digit or checksum


def print_main_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def print_bank_menu():
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")


def generate_card_number():
    """
    :return: 16 chars long digit of digits
    """

    card_num_string = "400000"                        # 6 digits long
    card_num_string += generate_account_number()      # 15-digits long

    # Generate check number from current card numbers
    card_numbers = [int(x) for x in card_num_string]
    processed_nums = process_numbers(card_numbers)
    check_number = get_check_digit(processed_nums)

    card_num_string += str(check_number)              # 16 digits long
    return card_num_string


def generate_account_number():
    account_number = ""
    for _ in range(0, 9):
        account_number += str(random.randint(0, 9))
    return account_number


def process_numbers(numbers):
    """
    Luhn algorithm
    1. Drop the last digit
    2. Multiply odd digits by 2
    3. Subtract numbers over 9 by 9
    4. Add all numbers
    5. Modulus 10

    Result: if 0, return true, otherwise return false
    """

    # Not necessary when auto generating
    # numbers.pop()

    for i in range(0, len(numbers), 2):
        numbers[i] *= 2
    numbers = [x - 9 if x > 9 else x for x in numbers]
    return numbers


def get_check_digit(card_nums):
    num_sum = sum(card_nums)

    check_digit = 0
    while True:
        if (num_sum + check_digit) % 10 == 0:
            break
        check_digit += 1
    return check_digit


def generate_pin():
    pin = ""
    for _ in range(0, 4):
        pin += str(random.randint(0, 9))
    return pin


def login(card_num, pin):
    while True:
        print_bank_menu()
        login_input = int(input())
        if login_input == 0:
            return False
        elif login_input == 1:
            print("Balance: 0")
        elif login_input == 2:
            return True


# Program entry point
bank_db = DatabaseManager()
bank_db.setup_table()

card_number = None
card_pin = None

is_running = True
while is_running:
    print_main_menu()
    user_input = int(input())

    if user_input == 0:
        is_running = False
        print("\nBye!")
    elif user_input == 1:
        card_number = generate_card_number()
        card_pin = generate_pin()
        print("\nYour card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(card_pin)
        print()
        bank_db.insert_new_data(card_number, card_pin)
    elif user_input == 2:
        print("Enter your card number:")
        user_card = input()
        print("Enter your PIN:")
        user_pin = input()
        if user_card == card_number and user_pin == card_pin:
            print("\nYou have successfully logged in!")
            is_running = login(card_number, card_pin)
        else:
            print("\nWrong card number or PIN!")


bank_db.close()
