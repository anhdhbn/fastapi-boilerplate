from typing import Generic, Optional, TypeVar

from asgi_correlation_id import correlation_id
from humps import camelize
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from app.i18n.errors import ErrorCode
from app.i18n.lang import MultiLanguage

T = TypeVar("T")


def to_camel(string):
    return camelize(string)


class ResponseSchemaBase(BaseModel):
    __abstract__ = True
    
    code: str = ''
    message: str = ''
    trace_id: Optional[str] = ''

    class Config:
        arbitrary_types_allowed = True
        alias_generator = to_camel
        allow_population_by_field_name = True
    
    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        self.trace_id = correlation_id.get()
        return self

    def success_response(self, lang: MultiLanguage):
        self.code = ErrorCode.SUCCESS_0000
        self.message = lang.get(ErrorCode.SUCCESS_0000)
        self.trace_id = correlation_id.get()
        return self


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None
    
    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        self.trace_id = correlation_id.get()
        return self
    
    def success_response(self, data: T, lang: MultiLanguage):
        self.code = ErrorCode.SUCCESS_0000
        self.message = lang.get(ErrorCode.SUCCESS_0000)
        self.data = data
        self.trace_id = correlation_id.get()
        return self


class MappingByFieldName(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        use_enum_values = True


class PaginationReq(MappingByFieldName):
    page: Optional[int] = Field(default=1, ge=1)
    page_size: Optional[int] = Field(default=10, ge=1, le=1000)


class PaginationResp(MappingByFieldName):
    current_page: int
    page_size: int
    total_items: int
