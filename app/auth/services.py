import uuid

import bcrypt
import jwt

from app.exceptions.application import DomainException
from app.auth import schemas
from app.user.domain import User
from app.utils.mapper import EntityNotFound


class Registrar:

    def __init__(self, user_mapper, password_hasher, validator):
        self.user_mapper = user_mapper
        self.password_hasher = password_hasher
        self.validator = validator

    async def register(self, user_dto):
        self.validator.validate(user_dto, schemas.CreateUserSchema)

        user = await self.user_mapper.find_one_by(
            username=user_dto.username
        )
        if user is not None:
            raise DomainException(
                f"User with username '{user_dto.username}' already exists.",
                {"username": user_dto.username}
            )

        hashed_password = await self.password_hasher.generate(user_dto.password)

        user = User(
            id=user_dto.id,
            username=user_dto.username,
            password=hashed_password,
        )

        return user


class PasswordHasher:

    def __init__(self, process_executor):
        self.process_executor = process_executor

    async def generate(self, password):
        return await self.process_executor.run(
            self._generate,
            password
        )

    @staticmethod
    def _generate(password):
        password = password.encode(encoding='utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt).decode()
        return hashed_password


class Authenticator:

    def __init__(
            self,
            user_mapper,
            password_checker,
            token_generator,
            validator
            ):
        self.user_mapper = user_mapper
        self.password_checker = password_checker
        self.token_generator = token_generator
        self.validator = validator

    async def authenticate(self, authenticate_user_dto) -> str:
        self.validator.validate(authenticate_user_dto, schemas.AuthenticateUserSchema)

        user = await self.user_mapper.find_one_by(username=authenticate_user_dto.username)
        if user is None:
            raise EntityNotFound(
                f"There is no user with username {authenticate_user_dto.username}.",
                {'username': authenticate_user_dto.username}
            )
        if not await self.password_checker.check(user, authenticate_user_dto.password):
            raise DomainException("Password is invalid.")

        token = await self.token_generator.generate(
            {'user_id': user.id}
        )

        user.token = token
        await self.user_mapper.update(user)

        return token


class PasswordChecker:

    def __init__(self, process_executor):
        self.process_executor = process_executor

    async def check(self, user, password):
        return await self.process_executor.run(
            self._check,
            password,
            user.password
        )

    @staticmethod
    def _check(password, hashed_password):
        return bcrypt.checkpw(
            password.encode(encoding='utf-8'),
            hashed_password.encode(encoding='utf-8')
        )


class TokenGenerator:

    def __init__(self, process_executor, config):
        self.process_executor = process_executor
        self.config = config

    async def generate(self, payload):
        return await self.process_executor.run(
            self._generate,
            payload,
            self.config['expiration_time'],
            self.config['secret'],
            self.config['algorithm']
        )

    @staticmethod
    def _generate(payload, expiration_time, secret, algorithm):
        token = jwt.encode(
            {
                **payload,
                'salt': str(uuid.uuid4())
            },
            secret,
            algorithm=algorithm
        )
        return token.decode(encoding='utf-8')
