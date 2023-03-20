from datetime import datetime
from importlib import import_module
from typing import Any, List, Union

from pydantic import BaseModel, Extra, validator

from server.services.formatters import format_datetime_into_isoformat, format_dict_key_to_camel_case


class BaseDocument(BaseModel):
    class Config:
        orm_mode: bool = True
        use_enum_values: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime: format_datetime_into_isoformat}


class BaseTokenAPI(BaseModel):
    class Config:
        allow_population_by_field_name: bool = True


class BaseAPI(BaseTokenAPI):
    class Config:
        orm_mode: bool = True
        alias_generator: Any = format_dict_key_to_camel_case


class BaseRequest(BaseAPI):
    class Config:
        extra = Extra.forbid


class BaseResponse(BaseAPI):
    id: str

    @validator("id", pre=True)
    def convert_id(cls, v):
        return str(v)


class MapperSchema(BaseModel):
    name: str
    collections: List[str]

    @validator("collections")
    def validate_class_path(cls, value):
        for path in value:
            try:
                module_name, class_name = path.rsplit(".", 1)
                module = import_module(module_name)
                _ = getattr(module, class_name)
            except (ValueError, ImportError, AttributeError):
                raise ValueError(f"Invalid class path: {path}")
        return value


class MessageResponseSchema(BaseAPI):
    loc: Union[List[str], None] = None
    msg: str
    type: Union[str, None] = None


class HealthResponse(BaseAPI):
    APP_NAME: str
    MODE: str
    DEBUG: bool
