from pydantic import BaseModel
from typing import List


class controller_schema(BaseModel):
    name: str


class pin_schema(BaseModel):
    name: str


class pin_update_schema(BaseModel):
    state: int


class pin_return_schema(BaseModel):
    name: str
    state: int
    uuid: str

    class Config:
        orm_mode = True


class controller_return_schema(BaseModel):
    name: str
    uuid: str
    pins: List[pin_return_schema] = []

    @staticmethod
    def list_parse(fields: List) -> List:
        schemas: List[controller_return_schema] = []
        for field in fields:
            schemas.append(controller_return_schema.from_orm(field))
        return schemas

    class Config:
        orm_mode = True
