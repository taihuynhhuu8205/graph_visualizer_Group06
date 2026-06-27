
from models.graph import Graph


def build_graph_from_json(data):

    nodes = [n['id'] for n in data.get('nodes', [])]
    edges = data.get('edges', [])
    directed = data.get('directed', False)
    weighted = data.get('weighted', False)

    return Graph(nodes, edges, directed, weighted)


def create_step(step_num, **kwargs):

    step = {
        'step': step_num,
        'current_node': kwargs.get('current_node', None),
        'current_edge': kwargs.get('current_edge', None),
        'visited': list(kwargs.get('visited', [])),
        'queue_or_stack': list(kwargs.get('queue_or_stack', [])),
        'distances': dict(kwargs.get('distances', {})),
        'mst_edges': list(kwargs.get('mst_edges', [])),
        'max_flow': kwargs.get('max_flow', None),
        'euler_path': list(kwargs.get('euler_path', [])),
        'partition': dict(kwargs.get('partition', {})),
        'path': list(kwargs.get('path', [])),
        'total_weight': kwargs.get('total_weight', None),
        'description': kwargs.get('description', ''),
        'highlight_line': kwargs.get('highlight_line', -1),
        'node_colors': dict(kwargs.get('node_colors', {})),
        'edge_colors': dict(kwargs.get('edge_colors', {})),
    }
    return step
