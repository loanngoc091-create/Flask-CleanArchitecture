# src/application/dto/auth_result.py

class AuthResult:
    def __init__(self, access_token: str, refresh_token: str, role: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.role = role
