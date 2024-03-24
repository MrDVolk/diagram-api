import re
import ast
import pygraphviz as pgv

class Parser:
    def __init__(self, config: dict = None):
        if config is None:
            config = dict()
            
        self.config = config
        self.config.setdefault('render_image', False)
        self.config.setdefault('delimiter', '###')
        self.config.setdefault('definitions_regex', r"(.*)\[\"(.*?)\"\]({('\w+':'\w+',? ?)+})?")
        self.config.setdefault('edges_regex', r"(\w+) --> (\w+)({('\w+':'\w+',? ?)+})?")

    def to_graph(self, input_string: str) -> pgv.AGraph:
        delimiter = self.config['delimiter']
        definitions, edges = input_string.split(delimiter)
        definitions, edges = definitions.strip(), edges.strip()

        graph_object = pgv.AGraph(directed=True)

        for definition in definitions.split('\n'):
            match = re.match(self.config['definitions_regex'], definition)
            if match:
                node = match.group(1)
                label = match.group(2)
                attributes = ast.literal_eval(match.group(3)) if match.group(3) else {}

                graph_object.add_node(node, label=label, **attributes)

        for edge in edges.split('\n'):
            match = re.match(self.config['edges_regex'], edge)
            if match:
                source, target = match.group(1), match.group(2)
                attributes = ast.literal_eval(match.group(3)) if match.group(3) else {}
                label = attributes.get('label', '')
                edge_type = attributes.get('type', 'normal')

                graph_object.add_edge(source, target, label=label, type=edge_type)

        if self.config['render_image']:
            graph_object.layout(prog='dot')
            graph_object.draw('diagram.png')

        return graph_object
