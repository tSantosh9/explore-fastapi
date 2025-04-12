from sqlmodel import SQLModel, create_engine
from database import config

engine = create_engine(config.DB_URL, echo=True)

def init_database():
    SQLModel.metadata.create_all(engine)