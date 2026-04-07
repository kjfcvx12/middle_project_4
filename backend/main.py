from fastapi import FastAPI

from dotenv import load_dotenv


load_dotenv(dotenv_path="../../.env")

app=FastAPI()




#uvicorn main:app --port=8081 --reload