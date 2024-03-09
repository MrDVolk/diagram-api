import __init__
from pydantic import BaseModel
from fastapi import FastAPI
from src.dgrm import upload_figure


app = FastAPI()

class ConvertRequest(BaseModel):
    input_string: str


@app.get("/")
async def root() -> dict:
    return {"available": True}


@app.post("/convert")
async def convert(request_data: ConvertRequest) -> dict:
    return {"link": upload_figure(request_data.input_string)}
