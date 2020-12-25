from pydantic.main import BaseModel


class auth_schema(BaseModel):
    key: str

    class Config:
        orm_mode = True
