from marshmallow import Schema, fields

class AuthRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class AuthResponseSchema(Schema):
    access_token = fields.String()
    role = fields.String()
