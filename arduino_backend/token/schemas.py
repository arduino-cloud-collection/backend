from pydantic import BaseModel
from typing import List


class token_schema(BaseModel):
    name: str
    controller_id: str


class token_return_schema(BaseModel):
    name: str
    controller_id: str
    uuid: str

    @staticmethod
    def list_parse(fields: List) -> List:
        schemas: List[token_return_schema] = []
        for field in fields:
            schemas.append(token_return_schema.from_orm(field))
        return schemas

    class Config:
        orm_mode = True


class token_update_schema(BaseModel):
    name: str
