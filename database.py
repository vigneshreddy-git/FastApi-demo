

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

db_url = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password="vignu0987@",
    host="localhost",
    port=5432,
    database="telusko",
)


engine=create_engine(db_url)

session= sessionmaker(autocommit=False,autoflush=False,bind=engine)