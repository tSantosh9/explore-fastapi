from pydantic import BaseModel, Field

class Image(BaseModel):
    title: str
    url: str

class Employee(BaseModel):
    emp_id: str
    first_name: str
    last_name: str
    email: str = Field(min_length=9, max_length=90, pattern=r"[a-zA-Z0-9]@[a-zA-Z]+\.com")
    # Making it optional
    dept_id: str = Field(default=None)
    # Making it optional
    images: list[Image] = Field(default=None)


class UserIn(BaseModel):
    user_id: str
    user_name: str
    password: str

class UserOut(BaseModel):
    user_id: str
    user_name: str