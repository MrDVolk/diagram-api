import pygraphviz as pgv

class Parser:
    def __init__(self, config: dict = None):
        if config is None:
            config = dict()
            
        self.config = config
        self.config.setdefault('delimiter', '###')
        self.config.setdefault('edge_connector', ' --> ')
        self.config.setdefault('edge_label_delimiter', '::')

    def to_graph(self, input_string: str) -> pgv.AGraph:
        delimiter = self.config['delimiter']
        definitions, edges = input_string.split(delimiter)
        definitions, edges = definitions.strip(), edges.strip()

        graph_object = pgv.AGraph(directed=True)

        for definition in definitions.split('\n'):
            if '[' in definition:
                node, label = definition.split('[')
                label = label.strip('\"[]')
            else:
                node = definition
                label = node
            graph_object.add_node(node, label=label)

        for edge in edges.split('\n'):
            connections = edge
            label, edge_type = '', 'normal'

            if self.config['edge_label_delimiter'] in edge:
                connections, label = edge.split(self.config['edge_label_delimiter'])
                if '[' in label:
                    label, edge_type = label.split('[type=')
                    edge_type = edge_type.strip(']')

            source, target = connections.split(self.config['edge_connector'])
            graph_object.add_edge(source, target, label=label, type=edge_type)

        return graph_object