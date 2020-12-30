import sqlite3


class DatabaseManager:

    def __init__(self):
        self.db_name = "./card.s3db"
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as error_msg:
            print(error_msg)

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

    def insert_new_card(self, a_number, a_pin):
        """Inserts a row into the table card"""
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

    def update_balance(self, a_amount, a_number, a_pin):
        balance = self.get_balance(a_number, a_pin)[0]
        balance += a_amount
        data = (balance, a_number, a_pin)

        try:
            self.cursor.execute("UPDATE card SET balance = ? WHERE number=? AND pin=?", data)
            self.conn.commit()
        except Exception as e:
            print("No such account.")

    def get_target_account(self, a_card_number):
        data = (a_card_number,)

        account = None

        try:
            self.cursor.execute("SELECT * FROM card WHERE number=?", data)
            account = self.cursor.fetchone()
        except Exception as e:
            print("No such account.")

        return account

        # if account is None:
        #     return False
        # return True

    def display_all_data(self):
        """Method to display all rows in database for debugging purposes"""
        for row in self.cursor.execute("SELECT * FROM card"):
            print(f"id: {row[0]} | number: {row[1]} | pin: {row[2]} | balance: {row[3]}")
            # print(row)

    def close(self):
        # TEST: Refresh balance to zero of all cards
        # reset = (0,)
        # self.cursor.execute("UPDATE card SET balance = ?", reset)
        # self.conn.commit()

        self.cursor.close()
        self.conn.close()

    def get_account(self, card_num, card_pin):
        data = (card_num, card_pin)
        account = None

        try:
            self.cursor.execute("SELECT * FROM card WHERE number=? AND pin=?", data)
            account = self.cursor.fetchone()
            # print(f"Inside database, account: {account}")
        except Exception as e:
            print("No such account.")
        return account

    def delete_table_rows(self):
        try:
            self.cursor.execute("DELETE FROM card")
            self.conn.commit()
        except:
            print("Failed to delete all table data")

    def close_account(self, a_number, a_pin):
        data = (a_number, a_pin)
        try:
            self.cursor.execute("DELETE FROM card WHERE number=? AND pin=?", data)
            self.conn.commit()
        except:
            print("Failed to delete row")
