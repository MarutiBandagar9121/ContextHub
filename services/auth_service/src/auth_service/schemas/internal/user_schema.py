from typing import List

from pydantic import BaseModel

class UserIdsRequestSchema(BaseModel):
    user_ids:List[int]

class UserDetails(BaseModel):
    user_id:int
    first_name:str
    last_name:str
    email:str

    model_config = {
        "from_attributes": True
    }
