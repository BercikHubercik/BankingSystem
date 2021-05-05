# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Write your code here
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class User:
    def __init__(self, id=0, card_number_str='', Pin='', balance=0):
        self.user_id = id
        self.card_number = [4, 0, 0, 0, 0, 0]
        self.card_number_str = card_number_str
        self.pin = Pin
        self.balance = balance


class Database:
    @staticmethod
    def create_database():
        cur.execute('CREATE TABLE IF NOT EXISTS card('
                    'id INTEGER,'
                    'number TEXT,'
                    'pin TEXT,'
                    'balance INTEGER DEFAULT 0);')
        conn.commit()

    @staticmethod
    def add_user(user_id, card_number, pin, balance=0):
        cur.execute('INSERT INTO card VALUES ({}, {}, {}, {})'.format(user_id, card_number, pin, balance))
        conn.commit()

    @staticmethod
    def change_balance(card_number, income):
        cur.execute('UPDATE card SET balance = balance + {} WHERE number = {}'.format(income, card_number))
        conn.commit()

    @staticmethod
    def is_card_number(card_number):
        cur.execute('SELECT number FROM card WHERE number = {}'.format(card_number))
        number = cur.fetchall()
        if number is None:
            return True
        else:
            return False

    @staticmethod
    def get_pin_by_number(card_number):
        cur.execute('SELECT pin FROM card WHERE number = {}'.format(card_number))
        pin = cur.fetchone()
        # print(type(pin), pin[0])
        if pin is None:
            return None
        else:
            return pin[0]

    @staticmethod
    def get_balance_by_card(card_number):

        cur.execute('SELECT balance FROM card WHERE number = {}'.format(card_number))
        balance = cur.fetchone()

        return balance[0]

    @staticmethod
    def delete_user(user):
        cur.execute('DELETE FROM card WHERE number = {}'.format(user.card_number_str))
        conn.commit()

    @staticmethod
    def get_max_id():
        cur.execute('SELECT MAX(id) FROM card')
        max_id = cur.fetchall()
        max_id = max_id[0][0]
        if max_id is None:
            return 0
        else:
            return max_id


class System:
    def __init__(self):
        self.main_menu_choice = None
        self.users = []

    @staticmethod
    def exit_system():
        print('Bye!')

    @staticmethod
    def create_account():
        user = User()
        user.user_id = Database.get_max_id() + 1
        System.generate_card_number(user)
        for _ in range(4):
            user.pin += str(random.randint(0, 9))
        Database.add_user(user.user_id, user.card_number_str, user.pin)
        print('Your card number:')
        print(user.card_number_str)
        print('Your card Pin:')
        print(user.pin)
        System.login_menu()

    @staticmethod
    def generate_card_number(user):
        for _ in range(9):
            user.card_number.append((random.randint(0, 9)))

        check_sum = System.calculate_check_sum(user.card_number)
        user.card_number.append(check_sum)
        user.card_number_str = ''.join([str(elem) for elem in user.card_number])

    @staticmethod
    def calculate_check_sum(card_number):
        if len(card_number) == 15:
            temp = list(card_number[:])
        elif len(card_number) == 16:
            temp = list(card_number[:-1])
        temp = [int(i) for i in temp]
        for i in range(0, 15, 2):
            temp[i] *= 2
        for i in range(len(temp)):
            if temp[i] > 9:
                temp[i] -= 9
        added = sum(temp)
        check_sum = added % 10
        if check_sum != 0:
            check_sum = 10 - check_sum
        return check_sum

    @staticmethod
    def login():
        entered_card = input('Enter your card number')
        entered_pin = input('Enter your PIN')

        if Database.get_pin_by_number(entered_card) == entered_pin:
            print("You have successfully logged in!")
            user = User()
            user.card_number_str = entered_card
            user.pin = entered_pin
            System.main_menu(user)
        else:
            print('Wrong card number or PIN!')
            System.login_menu()

    @staticmethod
    def main_menu(user):
        print('1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit')
        choice = int(input())

        if choice == 1:
            print('Balance: {}'.format(Database.get_balance_by_card(user.card_number_str)))
            System.main_menu(user)
        elif choice == 2:
            income = input('Enter income:')
            Database.change_balance(user.card_number_str, income)
            System.main_menu(user)
        elif choice == 3:
            System.do_transfer(user)
            System.main_menu(user)
        elif choice == 4:
            Database.delete_user(user)
            System.login_menu()
        elif choice == 5:
            print('You have successfully logged out!')
            System.login_menu()
        elif choice == 0:
            System.exit_system()
            return

    @staticmethod
    def do_transfer(user):
        receiver_card = input('Enter card number')
        if user.card_number_str == receiver_card:
            print("You can't transfer money to the same account!")
        elif System.calculate_check_sum(receiver_card) != int(receiver_card[-1]):
            print('Probably you made a mistake in the card number. Please try again!')
            System.do_transfer(user)
        elif Database.is_card_number(receiver_card):
            print('Such a card does not exist.')
            System.do_transfer(user)

        transfer_amount = float(input('Enter how much money you want to transfer:'))
        if Database.get_balance_by_card(user.card_number_str) < transfer_amount:
            print('Not enough money!')
        else:
            Database.change_balance(user.card_number_str, -transfer_amount)
            Database.change_balance(receiver_card, transfer_amount)

    @staticmethod
    def login_menu():
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        main_menu_choice = int(input())
        if main_menu_choice == 1:
            System.create_account()
        elif main_menu_choice == 2:
            System.login()
        elif main_menu_choice == 0:
            System.exit_system()


system = System()
Database.create_database()
system.login_menu()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
