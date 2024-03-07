from fastapi import FastAPI
from dgrm import get_json

app = FastAPI()


@app.get("/")
async def root():
    return {"available": True}


@app.post("/convert")
async def convert(input_string: str):
    return get_json(input_string)
