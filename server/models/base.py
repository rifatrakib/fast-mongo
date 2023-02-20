from datetime import datetime
from typing import Any, List

from pydantic import BaseModel, Extra, validator

from server.services.formatters import format_datetime_into_isoformat, format_dict_key_to_camel_case


class BaseDocument(BaseModel):
    class Config:
        orm_mode: bool = True
        use_enum_values: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime: format_datetime_into_isoformat}


class BaseRequest(BaseModel):
    class Config:
        extra = Extra.forbid
        allow_population_by_field_name: bool = True
        alias_generator: Any = format_dict_key_to_camel_case


class BaseResponse(BaseModel):
    id: str

    class Config:
        allow_population_by_field_name: bool = True
        alias_generator: Any = format_dict_key_to_camel_case

    @validator("id", pre=True)
    def convert_id(cls, v):
        return str(v)


class DatabaseMapper(BaseModel):
    name: str
    collections: List[str]


class MapperSchema(BaseModel):
    databases: List[DatabaseMapper]
