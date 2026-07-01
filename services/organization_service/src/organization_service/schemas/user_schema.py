from pydantic import BaseModel

class UserServiceUserDetailsResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str

class AuthServiceRegisterResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str