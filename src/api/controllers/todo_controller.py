from swagger import spec
from flask import Blueprint, request, jsonify
bp = Blueprint("swagger", __name__)
@bp.route("/login", methods=["POST"])
def login():
    """
    ---
    post:
      tags:
        - Auth
      requestBody:
        required: true
        content:
          application/json:
            schema: LoginRequestSchema
      responses:
        200:
          description: OK
    """
    ...
