from pydantic import BaseModel

class ResponseDto(BaseModel):
    ok: bool = True