import __init__
import pygraphviz as pgv
from src.utils import convert_value

class Converter:
    def __init__(self, config: dict = None):
        if config is None:
            config = dict()
            
        self.config = config

    def to_json(self, graph: pgv.AGraph) -> dict:
        graph.layout(prog='dot')
        json_graph = {'v': '1.2', 's': {}}
        max_y_pos = max([
            int(float(node.attr['pos'].split(',')[1]))
            for node in graph.nodes()
        ])
        
        for node in graph.nodes():
            x, y = node.attr['pos'].split(',')
            x = convert_value(x, 'x')
            y = convert_value(y, 'y')

            height = convert_value(node.attr['height'], 'height')
            width = convert_value(node.attr['width'], 'width')

            label = node.attr['label']
            json_graph['s'][node] = {"id": node, "type": 2, "position": {"x": x, "y": max_y_pos-y}, "title": label, "w": width, "h": height}
        
        for edge in graph.edges():
            label = edge.attr['label']
            edge_type = edge.attr['type'] if 'type' in edge.attr else 'normal'
            match edge_type:
                case 'normal':
                    edge_class = "d-arw-e"
                case 'dash':
                    edge_class = "d-dash"
                case _:
                    edge_class = "d-arw-e"
                
            start, end = edge
            edge_id = f"{start}:{end}"
            json_graph["s"][edge_id] = {"id": edge_id, "type": 0, "s": {"s": start, "k": "bottom"}, "e": {"s": end, "k": "top"}, "title": label, "c": [edge_class]}
        
        return json_graph