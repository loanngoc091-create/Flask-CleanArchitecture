from marshmallow import Schema, fields

class LoginRequestSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
