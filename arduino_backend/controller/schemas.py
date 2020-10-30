from pydantic import BaseModel


class controller_schema(BaseModel):
    name: str


class pin_schema(BaseModel):
    name: str
