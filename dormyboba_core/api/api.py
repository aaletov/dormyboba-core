from pydantic import BaseModel

class InviteRegisterUserRequest(BaseModel):
    token: str
    userId: int