from pydantic import BaseModel, StringConstraints, EmailStr, model_validator, Field, field_validator
from typing import Optional, List, Annotated
from constants.roles import Roles
import datetime


NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
PasswordStr = Annotated[str, StringConstraints(
    min_length=8,max_length=20,pattern=r'^[A-Za-z0-9?@#$%^&*|:]+$'
)]

class TestUser(BaseModel):
    #  магический аттрибут для исключения модели из тестов pydantic
    __test__ = False
    email: EmailStr
    fullName: NonEmptyString
    password: PasswordStr
    passwordRepeat: PasswordStr
    roles: List[Roles] = Roles.USER
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    id: Optional[int] = None

    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.passwordRepeat:
            raise ValueError("Passwords don't match")
        return self

class Config:
    json_encoders = {
        Roles: lambda v: v.value  # Преобразуем Enum в строку
    }

class RegisterUserResponse(BaseModel):
    id: str
    email: EmailStr
    fullName: NonEmptyString
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="createdAt должен быть строкой в формате ISO 8601")
    id: Optional[str] = None

    @field_validator("createdAt")
    def validate_created_at(cls, v: str) -> str:
        s = v[:-1] + "+00:00" if isinstance(v, str) and v.endswith("Z") else v
        try:
            datetime.datetime.fromisoformat(s)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return v
