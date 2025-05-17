from src.controllers.controller import Controller
from src.util.dao import DAO

import re
emailValidator = re.compile(r'.*@.*')

class UserController(Controller):
    def __init__(self, dao: DAO):
        super().__init__(dao=dao)

    def get_user_by_email(self, email: str):
        """
        Given a valid email address of a existing account, 
        return the user object contained in the database associated 
        to that user.
        """
        if not email or not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Error: invalid email address')

        try:
            users = self.dao.find({'email': email})
        except Exception:
            raise Exception("Database error")

        if len(users) == 0:
            raise IndexError("User not found")

        if len(users) > 1:
            print(f'Error: more than one user found with mail {email}')

        return users[0]

    def update(self, id, data):
        try:
            update_result = super().update(id=id, data={'$set': data})
            return update_result
        except Exception as e:
            raise