import __init__
import requests
from src.parser import Parser
from src.converter import Converter


def upload_figure(input_string: str) -> str:
    json_object = convert_string_to_dgrm(input_string)
    response = requests.post("https://api.dgrm.net/api/e/c", json=json_object)
    result_id = response.content.decode('utf-8')
    return f"https://app.dgrm.net/?k={result_id}"


def convert_string_to_dgrm(input_string: str) -> dict:
    graph_object = Parser().to_graph(input_string)
    graph_json = Converter().to_json(graph_object)
    return graph_json
