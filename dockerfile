FROM python:3.10.13-slim-bookworm

WORKDIR /app
COPY . .

RUN apt-get update 
RUN apt-get install -y graphviz libgraphviz-dev

RUN pip install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port $PORT