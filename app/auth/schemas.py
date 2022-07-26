from marshmallow import (Schema, fields, validate)


class CreateUserSchema(Schema):
    id = fields.String(required=True)
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))


class AuthenticateUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
