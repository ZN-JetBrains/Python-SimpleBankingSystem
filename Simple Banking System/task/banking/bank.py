from enum import IntEnum
import random
import bank_database

# 16 digits long card number
# 1-6: IIN must be 400_000 (first six digits)
# 7-15: Account number: unique (9 digits)
# 16: Check digit or checksum


class MainMenu(IntEnum):
    Exit = 0
    CreateAccount = 1
    Login = 2


class BankMenu(IntEnum):
    Exit = 0
    ShowBalance = 1
    AddIncome = 2
    DoTransfer = 3
    CloseAccount = 4
    LogOut = 5


class NetBank:

    def __init__(self):
        self.card_num = None
        self.card_pin = None
        self.is_running = True
        self.bank_db = bank_database.DatabaseManager()
        self.bank_db.setup_table()
        random.seed()

    def print_main_menu(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

    def print_bank_menu(self):
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

    def print_card_creation(self):
        print("\nYour card has been created")
        print("Your card number:")
        print(self.card_num)
        print("Your card PIN:")
        print(self.card_pin)
        print()

    def generate_card_number(self):
        """
        :return: 16 chars long digit of digits
        """

        card_num_string = "400000"  # 6 digits long
        card_num_string += self.generate_account_number()  # 15-digits long

        # Generate check number from current card numbers
        card_numbers = [int(x) for x in card_num_string]
        processed_nums = self.process_numbers(card_numbers)
        check_number = self.get_check_digit(processed_nums)

        card_num_string += str(check_number)  # 16 digits long
        return card_num_string

    def generate_account_number(self):
        account_number = ""
        for _ in range(0, 9):
            account_number += str(random.randint(0, 9))
        return account_number

    def process_numbers(self, numbers):
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

    def get_check_digit(self, card_nums):
        num_sum = sum(card_nums)

        check_digit = 0
        while True:
            if (num_sum + check_digit) % 10 == 0:
                break
            check_digit += 1
        return check_digit

    def generate_pin(self):
        pin = ""
        for _ in range(0, 4):
            pin += str(random.randint(0, 9))
        return pin

    def is_card_num_valid(self, a_card_num_str):
        a_card_num_str = a_card_num_str.strip()
        card_number = [int(x) for x in a_card_num_str]

        # if len(card_number) != 16:
        #     return False

        check_digit = card_number.pop()
        card_number.reverse()

        processed_digits = []

        for index, digit in enumerate(card_number):
            if index % 2 == 0:
                doubled_digit = digit * 2

                if doubled_digit > 9:
                    doubled_digit -= 9

                processed_digits.append(doubled_digit)
            else:
                processed_digits.append(digit)

        check_sum = check_digit + sum(processed_digits)
        if check_sum % 10 != 0:
            return False
        return True

    def do_transfer(self):
        print("\nTransfer\nEnter card number:")
        input_card_number = input().strip()

        # Luhn algorithm test
        if not self.is_card_num_valid(input_card_number):
            print("\nProbably you made a mistake in the card number. Please try again!\n")
            return

        if input_card_number == self.card_num:
            print("\nYou can't transfer money to the same account!\n")
            return

        target_account = self.bank_db.get_target_account(input_card_number)

        if target_account is None:
            print("Such a card does not exist.\n")
            return

        print("Enter how much money you want to transfer:")
        money = int(input())
        balance = self.bank_db.get_balance(self.card_num, self.card_pin)[0]

        if money > balance:
            print("Not enough money!\n")
            return

        # Subtract money from user balance
        self.bank_db.update_balance(-money, self.card_num, self.card_pin)

        # Add money to target balance
        target_num = target_account[1]
        target_pin = target_account[2]
        target_balance = target_account[3]
        target_balance += money
        self.bank_db.update_balance(target_balance, target_num, target_pin)
        print("Success!\n")

    def login(self):
        while True:
            self.print_bank_menu()
            login_input = int(input())

            if login_input == BankMenu.Exit:
                self.is_running = False
                break
            elif login_input == BankMenu.ShowBalance:
                balance = self.bank_db.get_balance(self.card_num, self.card_pin)[0]
                print(f"\nBalance: {balance}\n")
            elif login_input == BankMenu.AddIncome:
                print("\nEnter income:")
                income = int(input())
                self.bank_db.update_balance(income, self.card_num, self.card_pin)
                print("Income was added!\n")
            elif login_input == BankMenu.DoTransfer:
                self.do_transfer()
            elif login_input == BankMenu.CloseAccount:
                self.bank_db.close_account(self.card_num, self.card_pin)
                self.card_num = None
                self.card_pin = None
                print("\nThe account has been closed!\n")
                break
            elif login_input == BankMenu.LogOut:
                print("\nYou have successfully logged out!\n")
                break

    def run(self):
        while self.is_running:
            self.print_main_menu()
            user_input = int(input())

            if user_input == MainMenu.Exit:
                self.is_running = False
            elif user_input == MainMenu.CreateAccount:
                self.card_num = self.generate_card_number()
                self.card_pin = self.generate_pin()
                self.print_card_creation()
                self.bank_db.insert_new_card(self.card_num, self.card_pin)
            elif user_input == MainMenu.Login:
                print("\nEnter your card number:")
                user_card = input()
                print("Enter your PIN:")
                user_pin = input()
                account = self.bank_db.get_account(user_card, user_pin)
                if account is None:
                    print("\nWrong card number or PIN!\n")
                    # print(f"account: {account}")
                else:
                    self.card_num = account[1]
                    self.card_pin = account[2]
                    print("\nYou have successfully logged in!\n")
                    self.login()

        self.bank_db.close()
        print("\nBye!")
