from pydantic import BaseModel

class Department(BaseModel):
    dept_id: str
    dept_name: str
