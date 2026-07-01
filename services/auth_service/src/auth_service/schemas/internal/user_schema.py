from typing import List

from pydantic import BaseModel

class UserIdsRequestSchema(BaseModel):
    user_ids:List[int]

class UserDetails(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
