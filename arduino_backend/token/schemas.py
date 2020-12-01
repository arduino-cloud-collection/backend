from pydantic import BaseModel


class token_schema(BaseModel):
    name: str
    controller_id: str


class token_return_schema(BaseModel):
    name: str
    controller_id: str
    uuid: str

    class Config:
        orm_mode = True
