
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = 'sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# import os
# from fastapi import FastAPI, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String, text
# from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from dotenv import load_dotenv
# from sqlalchemy.exc import SQLAlchemyError

# from sqlalchemy.orm import DeclarativeBase

# class Base(DeclarativeBase):
#     pass

# # Load environment variables
# load_dotenv()

# # Database connection details
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# # Create the database URL
# DATABASE_URL = f"oracle://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)

# # Create a sessionmaker
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class Base(DeclarativeBase):
#     pass

# def check_db_connection():
#     engine = create_engine(DATABASE_URL)
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1 FROM DUAL"))
#             for row in result:
#                 print("Connected to the database successfully!")
#                 return True
#     except SQLAlchemyError as e:
#         print(f"Error connecting to the database: {str(e)}")
#         return False
#     finally:
#         engine.dispose()

# if __name__ == "__main__":
#     check_db_connection()