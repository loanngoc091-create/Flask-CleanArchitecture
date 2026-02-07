from functools import wraps
from flask import request, jsonify, g
import jwt
from config import Config

def jwt_required():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Missing token"}), 401

            token = auth_header.replace("Bearer ", "").strip()

            try:
                payload = jwt.decode(
                    token,
                    Config.SECRET_KEY,
                    algorithms=["HS256"]
                )
                g.user = payload
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator
