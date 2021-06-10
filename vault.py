#/usr/bin/python3
#coding: utf-8


import sqlite3 as sql
import sys


class _PassManager:
    def __init__(self, db_name):
        self.db = sql.connect(db_name)
        self.cur = self.db.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vault (
                    service TEXT,
                    password TEXT
                    )""")

    def insert_service(self):
        service = input("Service: ").strip()
        password = input("Password: ").strip()
        self.cur.execute(f"SELECT service FROM vault WHERE service = '{service}'")
        if self.cur.fetchone() is None:
            self.cur.execute(f"INSERT OR IGNORE INTO vault VALUES (?, ?)", (service, password))
            print("Service data added successfully!")
            self.db.commit()
        else:
            print("These data are available.")

    def show_all(self):
        self.cur.execute("SELECT service FROM vault")
        if self.cur.fetchone() is None:
            print("DataBase is empty.")
        else:
            print("List of available data: ")
            for values in self.cur.execute("SELECT * FROM vault"):
                print(values)

    def select_service(self):
        while True:
            service = input("Type service title for searching: ").strip()
            self.cur.execute(F"SELECT service FROM vault WHERE service = '{service}'")
            if self.cur.fetchone():
                for value in self.cur.execute(F"SELECT service, password FROM vault WHERE service = '{service}'"):
                    print(value)
                break
            else:
                print(R"There is no such service. Create it.")
                break

    def update_service(self):
        while True:
            service = input("Update the data of the service with the title: ").strip()
            self.cur.execute(F"SELECT service FROM vault WHERE service = '{service}'")
            if self.cur.fetchone() is None:
                print("There is no such service. Try it again.")
                break

            else:
                what = input(R"Edit(type 'service' or 'password'): ").strip()
                if what == "service":
                    new_name = input(R"New title: ")
                    self.cur.execute(F"UPDATE vault SET service = '{new_name}' WHERE service = '{service}' ")
                    self.db.commit()
                    print("Title updated successfully!")
                    break

                elif what == "password":
                    new_pass = input("New password: ").strip()
                    self.cur.execute(F"UPDATE vault SET password = '{new_pass}' WHERE service = '{service}'")
                    self.db.commit()
                    print("Password updated successfully!")
                    break

                else:
                    print("Incorrect input. Try again.")

    def delete_service(self):
        while True:
            service = input(R"Delete the service: ").strrip()
            self.cur.execute(F"SELECT service FROM vault WHERE service = '{service}'")
            if self.cur.fetchone() is None:
                print(R"There is no such service. Try it again.")
                break
            else:
                self.cur.execute(F"DELETE FROM vault WHERE service = '{service}'")
                self.db.commit()
                print(R"Service was deleted.")
                break


def get_option(manager, option):
    options = {
        '1': manager.insert_service,
        '2': manager.show_all,
        '3': manager.select_service,
        '4': manager.update_service,
        '5': manager.delete_service,
        '6': sys.exit
    }

    return options.get(option, "This option does not exist")()


def _main():
    manage_pass = _PassManager("key-vault.db")
    while True:
        print("""
            What do you want to do? (Choose 1, 2, 3...)
            1. Add service data.
            2. Show the entire list of databases.
            3. Print data for the desired service.
            4. Update data of the existing service.
            5. Delete the service and its data.
            6. Exit.
            """)
        choice = input("Type: ")
        option = get_option(manage_pass, choice)


if __name__ == "__main__":
    _main()
