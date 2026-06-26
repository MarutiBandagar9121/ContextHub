from pydantic import BaseModel

class UserServiceUserDetailsResponse(BaseModel):
    user_id:int
    first_name:str
    last_name:str
    email:str