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
            'darkblue': 'd-cl-dblue',
            'darkgray': 'd-cl-dgray'
        })
        self.config.setdefault('edge_mapping', {
            'normal': ['d-arw-e'],
            'reverse': ['d-arw-s'],
            'dash': ['d-dash', 'd-arw-e']
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
            y = convert_value(max_y_pos-int(float(y)), 'y')

            height = convert_value(node.attr['height'], 'height')
            width = convert_value(node.attr['width'], 'width')

            label = node.attr['label']
            color = self._map_color(node.attr.get('color', 'blue'))
            shape = self._map_shape(node.attr.get('dgrm_shape', 'rectangle'))
            json_graph['s'][node] = {
                'id': node, 
                'type': shape, 
                'position': {'x': x, 'y': y}, 
                'title': label, 
                'w': width, 'h': height, 
                'styles': [color]
            }
        
        for edge in graph.edges():
            label = edge.attr.get('label', '')
            edge_class = self._map_edge(edge.attr.get('type', 'normal'))

            start, end = edge
            edge_id = f'{start}:{end}'

            if (existing_edge_id := f'{end}:{start}') in json_graph['s']:
                existing_edge = json_graph['s'][existing_edge_id]
                reversed_edge_class = self._map_edge('reverse')
                existing_edge['c'].extend(reversed_edge_class)
                continue

            connection = self.connect_nodes(json_graph['s'][start], json_graph['s'][end], json_graph)
            json_graph['s'][edge_id] = {
                'id': edge_id,
                'type': 0,
                's': {'s': start, 'k': connection['start']},
                'e': {'s': end, 'k': connection['end']},
                'title': label,
                'c': edge_class
            }
        
        return json_graph
    
    def _map_color(self, color: str) -> str:
        return self.config['color_mapping'].get(color, 'd-cl-blue')
    
    def _map_shape(self, shape: str) -> int:
        return self.config['shape_mapping'].get(shape, 2)
    
    def _map_edge(self, edge_type: str) -> list[str]:
        return self.config['edge_mapping'].get(edge_type, ['d-arw-e'])

    def get_existing_connections(self, node_id: str, side: str, json_graph) -> int:
        possible_edges = [
            edge for edge in json_graph['s'] 
            if ':' in edge and node_id in edge.split(':')
        ]
        connection_count = 0
        for edge in possible_edges:
            edge_node = json_graph['s'][edge]
            if edge_node['s']['s'] == node_id and edge_node['s']['k'] == side:
                connection_count += 1
            elif edge_node['e']['s'] == node_id and edge_node['e']['k'] == side:
                connection_count += 1

        return connection_count
    
    def connect_nodes(self, start: dict, end: dict, json_graph: dict) -> dict:
        def is_occupied(node_id, side):
            return self.get_existing_connections(node_id, side, json_graph) > 3

        # Determine relative position
        dx = end['position']['x'] - start['position']['x']
        combined_width = start['w'] + end['w']
        if abs(dx) <= combined_width:
            dx = 0

        dy = end['position']['y'] - start['position']['y']
        avg_height = (start['h'] + end['h']) / 2
        if abs(dy) <= avg_height:
            dy = 0

        connection = {'start': '', 'end': ''}
        
        # Directly aligned cases
        if dx == 0:  # Vertically aligned
            if dy > 0:  # end is below start
                connection['start'] = 'bottom' if not is_occupied(start['id'], 'bottom') else 'left'
                connection['end'] = 'top' if connection['start'] == 'bottom' else 'left'
            else:  # end is above start
                connection['start'] = 'top' if not is_occupied(start['id'], 'top') else 'left'
                connection['end'] = 'bottom' if connection['start'] == 'top' else 'left'
        elif dy == 0:  # Horizontally aligned
            if dx > 0:  # end is to the right of start
                connection['start'] = 'right' if not is_occupied(start['id'], 'right') else 'top'
                connection['end'] = 'left' if connection['start'] == 'right' else 'top'
            else:  # end is to the left of start
                connection['start'] = 'left' if not is_occupied(start['id'], 'left') else 'top'
                connection['end'] = 'right' if connection['start'] == 'left' else 'top'
        else:  # Diagonally aligned
            if dx > 0:  # end is to the right of start
                if dy > 0:  # end is below start
                    connection["start"] = "bottom" if not is_occupied(start["id"], "bottom") else "right"
                    connection["end"] = "top" if connection["start"] == "bottom" else "left"
                else:  # end is above start
                    connection["start"] = "top" if not is_occupied(start["id"], "top") else "right"
                    connection["end"] = "bottom" if connection["start"] == "top" else "left"
            else:  # end is to the left of start
                if dy > 0:  # end is below start
                    connection["start"] = "bottom" if not is_occupied(start["id"], "bottom") else "left"
                    connection["end"] = "top" if connection["start"] == "bottom" else "right"
                else:  # end is above start
                    connection["start"] = "top" if not is_occupied(start["id"], "top") else "left"
                    connection["end"] = "bottom" if connection["start"] == "top" else "right"

        return connection
