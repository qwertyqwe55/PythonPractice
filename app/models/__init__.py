
import datetime
from enum import Enum
from typing import Union, Optional


from pydantic import BaseModel, conint, computed_field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


# class User(BaseModel):
#     name: str
#     age: int
#     adult: bool = None

class User(BaseModel):
    name: str
    age: conint(gt=0, lt=100)
    message: Optional[str] = None

    @computed_field
    @property
    def adult(self) -> bool:
        return self.age >= 18



class Meta(BaseModel):
    class Mapping(BaseModel):
        list_of_ids: list
        tags: list[str]

    last_modification: str
    list_of_skills : Optional[list[str]]
    mapping:Mapping


    @field_validator("last_modification", mode="before")
    @classmethod
    def non_iso_date(
            cls, value: str, info: FieldValidationInfo
    ) -> str:
        assert isinstance(value, str), info.field_name + " must be date as str 'dd/mm/yyyy'"
        return datetime.datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")


class BigJson(BaseModel):
    """Использует модель User."""
    user: User
    meta: Meta

# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
#
# class UserResponse(BaseModel):
#     pass
