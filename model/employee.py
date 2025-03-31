from pydantic import BaseModel, Field

class Employee(BaseModel):
    emp_id: int
    first_name: str
    last_name: str
    email: str = Field(min_length=9, max_length=90, pattern=r"[a-zA-Z0-9]@[a-zA-Z]+\.com")