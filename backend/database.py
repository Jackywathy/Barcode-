import sqlite3
import os
from backend.common import *
from backend.security import requires_level, UserTemplate, UserTemplateCollection, User, user_accessable
from backend.crypto import hash_password, check_password
from typing import Dict
from inspect import signature


class BaseTable:
    """Base class for tables"""
    table_name = NotImplemented
    def create_table(self):
        """Creates empty table """
        raise NotImplementedError

    @user_accessable
    @requires_level(PERMS_READ_USERS)
    def get_from_id(self, id):
        """
        Returns the data given from the id column
        :param id: int
        :return: List
        """
        return self.cursor.execute("""SELECT * FROM {} WHERE id=?""".format(self.table_name), (id,)).fetchall()

    def __init__(self, connection):
        """
        Base constructor for a table
        :type connection: sqlite3.Connection
        """
        self.connection = connection
        self.cursor = connection.cursor()
        if not self.cursor.execute("select 1 from sqlite_master WHERE type='table' and name='{}'".
                                            format(self.table_name)).fetchone():
            # users table does not exist, create the table
            print("Creating new {} table".format(self.table_name))
            self.create_table()

    def create_test_data(self):
        raise NotImplementedError

class UsersTable(BaseTable):
    """Contains all usernames, password hashes and auth. levels"""
    table_name = "users"
    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS {}""".format(self.table_name))
        self.cursor.execute("""
                   CREATE TABLE {} (
                       `id`        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                       `username`  TEXT NOT NULL UNIQUE,
                       `pass_hash`  TEXT NOT NULL,
                       `userlevel` INTEGER NOT NULL,
                       `twofactor` TEXT
                   )
               """.format(self.table_name,))

    def __init__(self, connection):
        super().__init__(connection)
        self.user_templates = UserTemplateCollection()
        self.read_users()

    def _add_user_to_collection(self, id, username, pass_hash, user_level, twofactor=None):
        template = UserTemplate(id, username, pass_hash, user_level, twofactor)
        self.user_templates.add_user(template)


    def read_users(self):
        """Reads all users from database and stores it in user_templates"""
        self.user_templates.clear()
        for user in self._get_users():
            self._add_user_to_collection(*user)


    def _write_usertemplate(self, username, password_input, user_level, twofactor=None, commit=True, add_to_self=True):
        """
        writes a new user to the user_table
        :param username: Username for new user
        :param password_input: unhashed password string for user
        :param permission: permission level
        :param twofactor: optional twofactor authentication (NOT IMPLEMENTED)
        :param commit: commit to database after each write
        :param add_to_self: adds to self.user_templates the new user

        """
        username = username.lower()
        self.cursor.execute("""
            INSERT INTO {} (
                username, pass_hash, userlevel
            ) VALUES (
                ?, ?, ?
            )
        """.format(self.table_name), (username, hash_password(password_input), user_level))


        if commit:
            self.connection.commit()
        if add_to_self:
            template = self._get_usertemplate(username)
            assert template is not None
            self._add_user_to_collection(template.id, template.username,
                                         template.pass_hash, template.user_level, template.two_factor)

    def _get_usertemplate(self, username):
        query =  self.cursor.execute("""
            SELECT * FROM {} WHERE username=?
        
        """.format(self.table_name), (username.lower(),)).fetchone()
        if query:
            id, username, pass_hash, level, twofactor = query
            return UserTemplate(id, username, pass_hash, level, twofactor)
        else:
            return None
        # since usernames are unique, query will return ['query',] or None


    def _get_users(self):
        """Gets all users in the user table"""
        return self.cursor.execute("""SELECT * FROM {}""".format(self.table_name)).fetchall()


    def commit(self):
        self.connection.commit()

    def create_test_data(self, overwrite=True):
        if overwrite:
            self.user_templates.clear()
            self.create_table()

        data = [
            ("jack", "password", PERMS_FULL),
            ("cheeze_whiz", "kraft", PERMS_READ_USERS),
            ("sqlite", "); drop table users; --", PERMS_FULL)

        ]
        for item in data:
            username, password, user_level = item
            self._write_usertemplate(username, password, user_level, commit=False)

        self.commit()

class ProductTable(BaseTable):
    """Contains all the barcodes and product information"""
    table_name = "products"
    # discounts is a json serialized dict: {"discount-reason": ['percent', 'number'], "discount-reason": ['total', 'number'] }
    def create_table(self):
        self.cursor.execute("""
                   CREATE TABLE {} (
                       `id`          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                       `barcode`     TEXT NOT NULL,
                       `name`        TEXT NOT NULL,
                       `description` TEXT NOT NULL,
                       `price`       TEXT NOT NULL,
                       `discounts`   TEXT NOT NULL,
                       `image`       BLOB 
                   )
               """.format(self.table_name))






class Database:
    """Holds all tables for all data used by this application"""
    tables = "users", "products"
    def __init__(self, file_path, create_if_empty=True, overwrite=False):
        """
        Creates
        :param file_path: a file path to the Database file, including filename and extension
        :param create_if_empty: creates empty database if the database doesn't already exist
        :param overwrite: always overwrite the database file

        :rtype file_path: str
        :rtype create_if_empty: str
        :rtype overwrite: str
        """
        self.path = file_path
        if file_path != ":memory:":
            # don't create any folders if it is a memory only database
            if create_if_empty and not os.path.isfile(self.path):
                # create a new database if it doesn't exist && asked for
                self.create_database(self.path)
            elif overwrite:
                self.create_database(self.path, remove=True)

        try:
            self.connection = sqlite3.connect(self.path)
        except sqlite3.OperationalError:
            raise ValueError("Supplied path invalid, please create using create_database")


        self.cursor = self.connection.cursor()

        self.user_table = UsersTable(self.connection)
        self.product_table = ProductTable(self.connection)

    @staticmethod
    def create_database(file_path, remove=False):
        """
        Creates an empty database at the file_path location.
        :param file_path: file path to write database
        :type file_path: str
        :param remove: to remove the file if it exists.
        :type remove: bool
        :rtype: Database
        """
        if file_path != ":memory:":
            print("Creating new database at {}".format(file_path))
            if os.path.isfile(file_path) and remove:
                os.remove(file_path)

            head, tail = os.path.split(file_path)
            if head == "":
                # if head is empty, then create it in the same directory, do nothing
                pass
            else:
                if not os.path.isdir(head):
                    os.makedirs(head)
            sqlite3.connect(file_path).close()

        return Database(file_path)

    def close(self):
        self.connection.close()

    def __str__(self):
        return "<backend.Database name={} tables=[{}]".format(self.path, " ".join(self.tables))

    def __repr__(self):
        return str(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def __enter__(self):
        return self

    def repl(self, data=()):
        """starts a read-eval-print-loop for database functions"""
        user = User.default_user

        count = 0

        if data:
            print(">>> ", end="")
            if count < len(data):
                ui = data[count]
            else:
                ui = ""
            count += 1
        else:
            ui = input(">>> ")



        def login(username, password):
            nonlocal user
            user = self.user_table.user_templates.login(password_input=password, username=username)
            return "logged in as: {}".format(user.username)
        login.args = 2

        def getuser():
            return user.username

        def get_all_usernames():
            sortedlist = (self.user_table.user_templates.get_usernames(user=user))
            return sortedlist

        commands = {
            "login": login,
            "getuser": getuser,
            "get-usernames": get_all_usernames
        }


        while ui:
            try:
                if len(ui.split()) > 1:
                    command, tail = ui.split(maxsplit=1)
                    args = tail.split()
                    func = commands.get(command.lower().strip(), lambda x: ("commands are: {}".format(",".join(commands.keys()))))
                    paramaters = signature(func).parameters

                    if len(args) != len(paramaters):
                        print("{} args, {} expected. Syntax is {} {}".format(len(args), len(paramaters), command, " ".join(paramaters.keys())))

                    else:
                        func(*args)


                else:
                    ret = commands.get(ui.lower().strip(), lambda: ("commands are: {}".format(", ".join(commands.keys()))))()
                    print(ret)





            except Exception as e:
                if data:
                    raise

                print(e)

            if data:
                print(">>> ", end="")
                if count < len(data):
                    ui = data[count]
                else:
                    ui = ""
                count += 1
            else:
                ui = input(">>> ")





if __name__ == "__main__":
    with Database("application.db") as data:
        data.user_table.create_test_data()
        data.repl()