from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    user_name: str
    email: str