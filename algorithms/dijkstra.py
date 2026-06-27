"""
Dijkstra — Thuật toán tìm đường đi ngắn nhất

Tìm đường đi ngắn nhất từ một đỉnh nguồn đến tất cả các đỉnh khác
(hoặc đến đỉnh đích cụ thể) trong đồ thị có trọng số không âm.
"""
import heapq

# Pseudocode cho hiển thị trên frontend
PSEUDOCODE = [
    "Dijkstra(G, start, end):",
    "  dist[v] = ∞ với mọi v",
    "  dist[start] = 0",
    "  prev[v] = null",
    "  PQ = {(0, start)}",
    "  while PQ không rỗng:",
    "    (d, u) = PQ.extractMin()",
    "    if u == end: return path",
    "    if d > dist[u]: continue",
    "    for mỗi v kề u:",
    "      alt = dist[u] + w(u,v)",
    "      if alt < dist[v]:",
    "        dist[v] = alt",
    "        prev[v] = u",
    "        PQ.insert((alt, v))",
]


def run(graph, start_node, end_node=None, **kwargs):
    """
    Chạy thuật toán Dijkstra.

    Args:
        graph: Graph object
        start_node: str — đỉnh nguồn
        end_node: str hoặc None — đỉnh đích (nếu cần tìm đường)

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0

    # Khởi tạo
    dist = {node: float('inf') for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    dist[start_node] = 0
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}
    visited = set()
    visited_order = []

    # Priority queue: (distance, node)
    pq = [(0, start_node)]

    # Bước 0: Khởi tạo
    step_num += 1
    desc = f'Khởi tạo Dijkstra từ đỉnh {start_node}'
    if end_node:
        desc += f' đến đỉnh {end_node}'
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [start_node],
        'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
        'description': desc,
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
    })

    node_colors[start_node] = 'processing'

    while pq:
        current_dist, current = heapq.heappop(pq)

        # Nếu khoảng cách hiện tại lớn hơn đã biết, bỏ qua
        if current_dist > dist[current]:
            continue

        visited.add(current)
        visited_order.append(current)
        node_colors[current] = 'visited'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': current,
            'current_edge': None,
            'visited': list(visited_order),
            'queue_or_stack': [n for _, n in pq],
            'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
            'description': f'Chọn đỉnh {current} (khoảng cách = {current_dist})',
            'highlight_line': 6,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
        })

        # Nếu tìm đến đích
        if end_node and current == end_node:
            # Truy vết đường đi
            path = []
            node = end_node
            while node is not None:
                path.append(node)
                node = prev[node]
            path.reverse()

            # Tô màu đường đi
            for n in path:
                node_colors[n] = 'result'
            for i in range(len(path) - 1):
                ek = f"{path[i]}-{path[i+1]}"
                rk = f"{path[i+1]}-{path[i]}"
                edge_colors[ek] = 'selected'
                if not graph.directed:
                    edge_colors[rk] = 'selected'

            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': end_node,
                'current_edge': None,
                'visited': list(visited_order),
                'queue_or_stack': [],
                'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
                'path': path,
                'total_weight': dist[end_node],
                'description': f'Tìm thấy đường đi: {" → ".join(path)}, tổng trọng số = {dist[end_node]}',
                'highlight_line': 7,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
            })

            return {
                'steps': steps,
                'pseudocode': PSEUDOCODE,
                'result': {
                    'path': path,
                    'total_weight': dist[end_node],
                    'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
                    'description': f'Đường đi ngắn nhất: {" → ".join(path)} (trọng số = {dist[end_node]})'
                }
            }

        # Duyệt các đỉnh kề
        neighbors = sorted(graph.get_neighbors(current))
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            weight = graph.get_weight(current, neighbor)
            alt = dist[current] + weight
            edge_key = f"{current}-{neighbor}"
            reverse_key = f"{neighbor}-{current}"

            edge_colors[edge_key] = 'considering'
            if not graph.directed:
                edge_colors[reverse_key] = 'considering'

            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current
                heapq.heappush(pq, (alt, neighbor))
                node_colors[neighbor] = 'processing'

                edge_colors[edge_key] = 'selected'
                if not graph.directed:
                    edge_colors[reverse_key] = 'selected'

                step_num += 1
                steps.append({
                    'step': step_num,
                    'current_node': current,
                    'current_edge': [current, neighbor],
                    'visited': list(visited_order),
                    'queue_or_stack': [n for _, n in pq],
                    'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
                    'description': f'Cập nhật dist[{neighbor}] = {alt} (qua {current})',
                    'highlight_line': 12,
                    'node_colors': dict(node_colors),
                    'edge_colors': dict(edge_colors),
                })
            else:
                step_num += 1
                steps.append({
                    'step': step_num,
                    'current_node': current,
                    'current_edge': [current, neighbor],
                    'visited': list(visited_order),
                    'queue_or_stack': [n for _, n in pq],
                    'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
                    'description': f'dist[{neighbor}] = {dist[neighbor]} ≤ {alt}, không cập nhật',
                    'highlight_line': 11,
                    'node_colors': dict(node_colors),
                    'edge_colors': dict(edge_colors),
                })

    # Hoàn thành (không có end_node hoặc không tìm thấy đường)
    for node in visited_order:
        node_colors[node] = 'result'

    step_num += 1
    final_desc = f'Dijkstra hoàn thành từ đỉnh {start_node}'
    if end_node and dist[end_node] == float('inf'):
        final_desc = f'Không tìm thấy đường đi từ {start_node} đến {end_node}'

    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': [],
        'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
        'description': final_desc,
        'highlight_line': -1,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
    })

    return {
        'steps': steps,
        'pseudocode': PSEUDOCODE,
        'result': {
            'distances': {k: ('∞' if v == float('inf') else v) for k, v in dist.items()},
            'description': final_desc
        }
    }
