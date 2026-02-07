from flasgger import swag_from
from flask import Blueprint, request, jsonify
import jwt
from config import Config
from datetime import datetime, timedelta
from application.services.auth_service import AuthService
from infrastructure.unit_of_work import UnitOfWork
from application.services.refresh_token_service import RefreshTokenService


bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Auth"],
    "summary": "Login system",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "admin@gmail.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "123456"
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Login success"
        },
        401: {
            "description": "Invalid credentials"
        }
    }
})
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    uow = UnitOfWork()
    refresh_token_service = RefreshTokenService(uow)

    with uow:
        auth_service = AuthService(
            user_repository=uow.users,
            refresh_token_service=refresh_token_service,
            unit_of_work=uow
        )

        user = auth_service.login(email, password)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "user_id": user.user_id,
        "role_code": user.role_code,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({
        "access_token": token,
        "user": {
            "user_id": user.user_id,
            "role": user.role_code
        }
    })