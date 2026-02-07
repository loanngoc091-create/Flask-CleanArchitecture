# src/domain/entities/user.py

import hashlib


class User:
    def __init__(self, user_id, email, password, role_code, role_name):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role_code = role_code
        self.role_name = role_name
        

    def verify_password(self, password: str) -> bool:
        return password == self.password_hash
