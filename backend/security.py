from backend.common import *
import backend.crypto as crypto

from typing import Dict
import functools


class InvalidPasswordException(Exception):
    def __str__(self):
        return "Password was wrong"
    def __repr__(self):
        return str(self)

class InvalidPermissionsException(Exception):
    def __init__(self, given, required):
        super().__init__()
        self.given = given
        self.required = required

    def __str__(self):
        return "Forbidden: level {}, required {}".format(self.given, self.required)

@functools.total_ordering
class UserTemplate:
    """A class that defines Users."""
    _next_unique = 0

    @property
    def next_unique(self) -> int:
        self._next_unique += 1
        return self.next_unique - 1

    def __init__(self, id, username, pass_hash, user_level, two_factor=None):
        self.id = id
        self.username = username
        self.pass_hash = pass_hash
        self.user_level = user_level
        self.two_factor = two_factor
        assert two_factor is None

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "<backend.security.UserTemplate name={}> user_level={}".format(self.username, self.user_level)

    def __repr__(self):
        return str(self)





class User:
    """A object that can be passed to a database to authenticate"""
    default_user = None
    def __str__(self):
        return "<backend.security.User username={}>".format(self.username)

    def __init__(self, password_input, user_template):
        """
        Creates a user object, given the passlib hashstring and an input password
        :type password_input: str
        :type user_template: UserTemplates
        """
        if crypto.check_password(password_input, user_template.pass_hash) is True:
            self.id = user_template.id
            self.user_level = user_template.user_level
            self.username = user_template.username
        else:
            raise InvalidPasswordException

    @staticmethod
    def get_default_user():
        user = type("e", (object,), {})()
        user.__class__ = User
        user.id = -1
        user.user_level = PERMS_NONE
        user.username = "default_user"
        return user
User.default_user = User.get_default_user()

def user_accessable(function):
    def wrapper(*args, user=User.default_user, **kwargs):
        function(*args, user=user, **kwargs)
    return wrapper


def requires_level(level_required):
    def real_decorator(function):
        def wrapper(*args,user, **kwargs):
            """
            :type user: User
            :returns:
            """
            if user.user_level < level_required:
                raise InvalidPermissionsException(user.user_level, level_required)
            return function(*args, **kwargs)

        return wrapper
    return real_decorator


class UserTemplateCollection:
    """Stores some UserTemplates"""
    def clear(self):
        self._username_to_user.clear()
        self._id_to_user.clear()
        self._users.clear()

    def __init__(self):
        self._id_to_user = {} # type: Dict[int: UserTemplate]
        self._username_to_user = {} # type: Dict[str: UserTemplate]
        self._users = []
        # usernames may not be unique!

    def get_user(self, id=None, username=None):
        """
        Gets a usertemplate, given id or username - only used for behind the scenes
        :type id: int
        :type username:
        :return:
        """
        if id is not None:
            return self._id_to_user[id]
        elif username is not None:
            return self._username_to_user[username]
        else:
            raise TypeError("either id or username must be set")

    @requires_level(PERMS_READ_USERS)
    def get_usernames(self):
        return sorted(self._users)

    def add_user(self, user):
        """
        Adds a UserTemplate to collection
        :param user: the usertemplate to be added
        :type user: UserTemplate
        """
        self._id_to_user[user.id] = user
        self._username_to_user[user.username] = user
        self._users.append(user)

    def __len__(self):
        return len(self._users)

    def login(self, password_input, id=None, username=None):
        """
        Gets a usertemplate, given id or username
        :param id: id to user
        :param password_input: password from user input
        :param username: username for user

        :type username: str
        :type id: int
        :type password_input: str
        :rtype: User
        """
        try:
            if id is not None:
                user =  User(password_input, self._id_to_user[id])

            elif username is not None:
                user = User(password_input, self._username_to_user[username])
            else:
                raise TypeError("either id or username must be set")
        except KeyError:
            raise KeyError("id or username supplied invalid: {}".format(id if id is not None else username))

        return user








