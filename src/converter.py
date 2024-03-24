import __init__
import pygraphviz as pgv
from src.utils import convert_value

class Converter:
    def __init__(self, config: dict = None):
        if config is None:
            config = dict()
            
        self.config = config
        self.config.setdefault('shape_mapping', {
            'circle': 1, 
            'rectangle': 2, 
            'diamond': 4
        })
        self.config.setdefault('color_mapping', {
            'red': 'd-cl-red',
            'orange': 'd-cl-orange',
            'green': 'd-cl-green',
            'blue': 'd-cl-blue',
            'dblue': 'd-cl-dblue',
            'dgray': 'd-cl-dgray'
        })
        self.config.setdefault('edge_mapping', {
            'normal': 'd-arw-e',
            'dash': 'd-dash'
        })

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
            color = self._map_color(node.attr.get('color', 'blue'))
            shape = self._map_shape(node.attr.get('shape', 'rectangle'))
            json_graph['s'][node] = {"id": node, "type": shape, "position": {"x": x, "y": max_y_pos-y}, "title": label, "w": width, "h": height, "c": [color]}
        
        for edge in graph.edges():
            label = edge.attr.get('label', '')
            edge_class = self._map_edge(edge.attr.get('type', 'normal'))
                
            start, end = edge
            edge_id = f"{start}:{end}"
            json_graph["s"][edge_id] = {"id": edge_id, "type": 0, "s": {"s": start, "k": "bottom"}, "e": {"s": end, "k": "top"}, "title": label, "c": [edge_class]}
        
        return json_graph
    
    def _map_color(self, color: str) -> str:
        return self.config['color_mapping'].get(color, 'd-cl-blue')
    
    def _map_shape(self, shape: str) -> int:
        return self.config['shape_mapping'].get(shape, 2)
    
    def _map_edge(self, edge_type: str) -> str:
        return self.config['edge_mapping'].get(edge_type, 'd-arw-e')
