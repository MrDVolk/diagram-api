import json
import pygraphviz as pgv


def get_json(input_string):
    delimiter = "###"
    definitions, edges = input_string.split(delimiter)
    definitions, edges = definitions.strip(), edges.strip()

    graph_object = pgv.AGraph(directed=True)
    
    # TODO: add figure type support
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
        
        if '::' in edge:
            connections, label = edge.split('::')
            if '[' in label:
                label, edge_type = label.split('[type=')
                edge_type = edge_type.strip(']')
            
        source, target = connections.split(' --> ')
        graph_object.add_edge(source, target, label=label, type=edge_type)

    graph_object.draw('diagram.png', prog='dot')
    
    graph_json = graph_to_json_with_positions(graph_object)
    json_string = json.dumps(graph_json)
    return json_string


def round_to_24(int_number: int, correction: int = 2) -> int:
    round_up = int_number % 24
    round_down = 24 - round_up
    rounded = int_number + round_down if round_down < round_up else int_number - round_up
    if rounded == 0:
        return 24 * correction
    return rounded * correction


def graph_to_json_with_positions(graph):
    graph.layout(prog='dot')
    json_graph = {'v': '1.2', 's': {}}
    max_y_pos = max([
        int(float(node.attr['pos'].split(',')[1]))
        for node in graph.nodes()
    ])
    
    for node in graph.nodes():
        pos = node.attr['pos']
        x, y = map(round_to_24, [int(float(val)) for val in pos.split(',')]) 
        height, width = map(round_to_24, [int(float(node.attr['height'])) * 100, int(float(node.attr['width'])) * 65])
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
