from pydantic import BaseModel

class UserDetails(BaseModel):
    user_id:int
    first_name:str
    last_name:str
    email:str

    model_config = {
        "from_attributes": True
    }