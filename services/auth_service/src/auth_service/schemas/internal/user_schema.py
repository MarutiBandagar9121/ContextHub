from typing import List

from pydantic import BaseModel

class UserIdsRequestSchema(BaseModel):
    user_ids:List[int]

class UserDetails(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str

class InternalRegisterRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str

class InternalRegisterResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
