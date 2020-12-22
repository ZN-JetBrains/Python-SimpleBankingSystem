import random
# 16 digit long card number
# 1-6: IIN must be 400_000 (first six digits)
# 7-15: Account number: unique (9 digits)
# 16: Check digit or checksum, anything atm


def print_main_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def print_bank_menu():
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")


def generate_card_number():
    card_num = "400000"
    card_num += generate_account_number()
    card_num += get_check_digit()
    return card_num


def generate_account_number():
    account_number = ""
    for _ in range(0, 9):
        account_number += str(random.randint(0, 9))
    return account_number


def get_check_digit():
    # Will use Luhn's algorithm later
    check_digit = str(random.randint(1, 9))
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
