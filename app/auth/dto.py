from dataclasses import dataclass


@dataclass
class CreateUserDto:
    id: str
    username: str
    password: str


@dataclass
class AuthenticateUserDto:
    username: str
    password: str
