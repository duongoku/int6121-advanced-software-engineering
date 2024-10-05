from pydantic import BaseModel


class AdminStatusResponse(BaseModel):
    status: str
    detail: str
