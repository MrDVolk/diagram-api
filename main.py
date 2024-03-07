from pydantic import BaseModel
from fastapi import FastAPI
from dgrm import get_json


app = FastAPI()

class ConvertRequest(BaseModel):
    input_string: str


@app.get("/")
async def root():
    return {"available": True}


@app.post("/convert")
async def convert(request_data: ConvertRequest):
    return {"output": get_json(request_data.input_string)}
