"""
Ford-Fulkerson — Thuật toán tìm luồng cực đại (Max Flow)

Sử dụng BFS (Edmonds-Karp) để tìm đường tăng luồng (augmenting path)
trong mạng luồng. Trả về luồng cực đại từ source đến sink.
"""
from collections import deque

# Pseudocode
PSEUDOCODE = [
    "Ford-Fulkerson(G, source, sink):",
    "  maxFlow = 0",
    "  Tạo residual graph = G",
    "  while tồn tại đường tăng luồng P (BFS):",
    "    Tìm bottleneck = min capacity trên P",
    "    for mỗi cạnh (u,v) trên P:",
    "      residual[u][v] -= bottleneck",
    "      residual[v][u] += bottleneck",
    "    maxFlow += bottleneck",
    "  return maxFlow",
]


def _bfs_find_path(residual, source, sink, nodes):
    """
    Tìm đường tăng luồng bằng BFS trong residual graph.

    Returns:
        (path, bottleneck) hoặc (None, 0) nếu không tìm thấy
    """
    visited = {source}
    queue = deque([(source, [source])])

    while queue:
        current, path = queue.popleft()
        if current == sink:
            # Tính bottleneck
            bottleneck = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                bottleneck = min(bottleneck, residual.get(u, {}).get(v, 0))
            return path, bottleneck

        for neighbor in sorted(nodes):
            cap = residual.get(current, {}).get(neighbor, 0)
            if cap > 0 and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, 0


def run(graph, start_node, end_node, **kwargs):
    """
    Chạy thuật toán Ford-Fulkerson (Edmonds-Karp).

    Args:
        graph: Graph object (có hướng, có trọng số — capacity)
        start_node: str — source
        end_node: str — sink

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}

    # Xây dựng residual graph
    residual = {}
    for node in graph.nodes:
        residual[node] = {}
    for node in graph.nodes:
        for neighbor, cap in graph.adj[node].items():
            residual[node][neighbor] = cap
            if neighbor not in residual:
                residual[neighbor] = {}
            if node not in residual[neighbor]:
                residual[neighbor][node] = 0

    max_flow = 0
    iteration = 0

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'max_flow': 0,
        'description': f'Khởi tạo Ford-Fulkerson: source={start_node}, sink={end_node}',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    while True:
        # Tìm đường tăng luồng
        path, bottleneck = _bfs_find_path(residual, start_node, end_node, graph.nodes)

        if path is None:
            break

        iteration += 1

        # Highlight đường tăng luồng
        path_node_colors = dict(node_colors)
        path_edge_colors = dict(edge_colors)
        for n in path:
            path_node_colors[n] = 'processing'
        for i in range(len(path) - 1):
            ek = f"{path[i]}-{path[i+1]}"
            path_edge_colors[ek] = 'considering'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': None,
            'current_edge': None,
            'visited': [],
            'queue_or_stack': path,
            'max_flow': max_flow,
            'path': path,
            'description': f'Lần {iteration}: Tìm thấy đường tăng luồng: {" → ".join(path)}, bottleneck = {bottleneck}',
            'highlight_line': 3,
            'node_colors': dict(path_node_colors),
            'edge_colors': dict(path_edge_colors),
            'distances': {},
        })

        # Cập nhật residual graph
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= bottleneck
            if v not in residual:
                residual[v] = {}
            residual[v][u] = residual.get(v, {}).get(u, 0) + bottleneck

            ek = f"{u}-{v}"
            path_edge_colors[ek] = 'selected'

        max_flow += bottleneck

        for n in path:
            path_node_colors[n] = 'visited'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': None,
            'current_edge': None,
            'visited': [],
            'queue_or_stack': [],
            'max_flow': max_flow,
            'path': path,
            'total_weight': bottleneck,
            'description': f'Cập nhật residual graph, luồng += {bottleneck}. Max Flow hiện tại = {max_flow}',
            'highlight_line': 7,
            'node_colors': dict(path_node_colors),
            'edge_colors': dict(path_edge_colors),
            'distances': {},
        })

        # Reset colors cho lần lặp tiếp
        node_colors = {n: 'default' for n in graph.nodes}
        edge_colors = dict(path_edge_colors)

    # Hoàn thành
    node_colors[start_node] = 'result'
    node_colors[end_node] = 'result'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'max_flow': max_flow,
        'description': f'Ford-Fulkerson hoàn thành! Max Flow = {max_flow}',
        'highlight_line': 8,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    return {
        'steps': steps,
        'pseudocode': PSEUDOCODE,
        'result': {
            'max_flow': max_flow,
            'description': f'Luồng cực đại từ {start_node} đến {end_node}: {max_flow}'
        }
    }
