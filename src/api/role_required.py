from functools import wraps
from flask import jsonify, g

def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if not g.get("user"):
                return jsonify({"error": "Unauthorized"}), 401

            user_role = g.user.get("role_code", "")

            if user_role.upper() != role.upper():
                return jsonify({
                    "error": "Forbidden",
                    "user_role": user_role,
                    "required_role": role
                }), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
