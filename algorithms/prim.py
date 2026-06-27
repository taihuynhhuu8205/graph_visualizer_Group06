"""
Prim — Thuật toán tìm cây khung nhỏ nhất (Minimum Spanning Tree)

Thuật toán Prim sử dụng priority queue để xây dựng MST
bằng cách lần lượt thêm cạnh có trọng số nhỏ nhất.
"""
import heapq

# Pseudocode
PSEUDOCODE = [
    "Prim(G, start):",
    "  MST = ∅",
    "  visited = {start}",
    "  PQ = các cạnh từ start",
    "  totalWeight = 0",
    "  while PQ không rỗng và |MST| < |V|-1:",
    "    (w, u, v) = PQ.extractMin()",
    "    if v đã thăm: continue",
    "    MST = MST ∪ {(u, v, w)}",
    "    totalWeight += w",
    "    visited = visited ∪ {v}",
    "    for mỗi cạnh (v, x, w') với x chưa thăm:",
    "      PQ.insert((w', v, x))",
    "  return MST, totalWeight",
]


def run(graph, start_node, **kwargs):
    """
    Chạy thuật toán Prim tìm MST.

    Args:
        graph: Graph object
        start_node: str — đỉnh bắt đầu

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0
    mst_edges = []
    total_weight = 0
    visited = set()
    visited_order = []
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}

    # Priority queue: (weight, source, target)
    pq = []

    # Bước 0: Khởi tạo
    visited.add(start_node)
    visited_order.append(start_node)
    node_colors[start_node] = 'visited'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': [],
        'mst_edges': [],
        'total_weight': 0,
        'description': f'Khởi tạo Prim từ đỉnh {start_node}',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Thêm các cạnh từ start vào PQ
    for neighbor in sorted(graph.get_neighbors(start_node)):
        weight = graph.get_weight(start_node, neighbor)
        heapq.heappush(pq, (weight, start_node, neighbor))

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': [f"({w},{s},{t})" for w, s, t in sorted(pq)],
        'mst_edges': [],
        'total_weight': 0,
        'description': f'Thêm các cạnh từ {start_node} vào priority queue',
        'highlight_line': 3,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Vòng lặp Prim
    while pq and len(mst_edges) < len(graph.nodes) - 1:
        weight, source, target = heapq.heappop(pq)

        edge_key = f"{source}-{target}"
        reverse_key = f"{target}-{source}"

        if target in visited:
            edge_colors[edge_key] = 'considering'
            if not graph.directed:
                edge_colors[reverse_key] = 'considering'

            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': target,
                'current_edge': [source, target],
                'visited': list(visited_order),
                'queue_or_stack': [f"({w},{s},{t})" for w, s, t in sorted(pq)],
                'mst_edges': list(mst_edges),
                'total_weight': total_weight,
                'description': f'Cạnh ({source},{target},w={weight}): đỉnh {target} đã thăm, bỏ qua',
                'highlight_line': 7,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })
            continue

        # Thêm cạnh vào MST
        visited.add(target)
        visited_order.append(target)
        mst_edges.append([source, target, weight])
        total_weight += weight
        node_colors[target] = 'visited'

        edge_colors[edge_key] = 'selected'
        if not graph.directed:
            edge_colors[reverse_key] = 'selected'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': target,
            'current_edge': [source, target],
            'visited': list(visited_order),
            'queue_or_stack': [f"({w},{s},{t})" for w, s, t in sorted(pq)],
            'mst_edges': list(mst_edges),
            'total_weight': total_weight,
            'description': f'Thêm cạnh ({source},{target},w={weight}) vào MST. Tổng = {total_weight}',
            'highlight_line': 8,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        # Thêm các cạnh mới từ target
        for neighbor in sorted(graph.get_neighbors(target)):
            if neighbor not in visited:
                w = graph.get_weight(target, neighbor)
                heapq.heappush(pq, (w, target, neighbor))

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': target,
            'current_edge': None,
            'visited': list(visited_order),
            'queue_or_stack': [f"({w},{s},{t})" for w, s, t in sorted(pq)],
            'mst_edges': list(mst_edges),
            'total_weight': total_weight,
            'description': f'Thêm các cạnh từ {target} vào priority queue',
            'highlight_line': 11,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

    # Hoàn thành
    for node in visited_order:
        node_colors[node] = 'result'

    step_num += 1
    mst_desc = ', '.join([f"({s},{t},w={w})" for s, t, w in mst_edges])
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': [],
        'mst_edges': list(mst_edges),
        'total_weight': total_weight,
        'description': f'Prim hoàn thành! MST: {mst_desc}. Tổng trọng số = {total_weight}',
        'highlight_line': 13,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    return {
        'steps': steps,
        'pseudocode': PSEUDOCODE,
        'result': {
            'mst_edges': mst_edges,
            'total_weight': total_weight,
            'description': f'MST (Prim): tổng trọng số = {total_weight}'
        }
    }
