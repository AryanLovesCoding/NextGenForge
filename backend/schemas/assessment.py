from pydantic import BaseModel

class Responses (BaseModel):
    responses: list[int]