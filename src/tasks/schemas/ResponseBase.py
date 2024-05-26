from pydantic import BaseModel


class ResponseBase(BaseModel):
    id: int
