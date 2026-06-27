"""
BFS — Breadth-First Search (Duyệt đồ thị theo chiều rộng)

Thuật toán duyệt đồ thị theo chiều rộng sử dụng hàng đợi (queue).
Trả về danh sách các bước để frontend hiển thị animation.
"""
from collections import deque


# Pseudocode cho hiển thị trên frontend
PSEUDOCODE = [
    "BFS(G, start):",
    "  Tạo queue Q",
    "  Đánh dấu start đã thăm",
    "  Thêm start vào Q",
    "  while Q không rỗng:",
    "    u = Q.dequeue()",
    "    Xử lý u",
    "    for mỗi v kề u:",
    "      if v chưa thăm:",
    "        Đánh dấu v đã thăm",
    "        Thêm v vào Q",
]


def run(graph, start_node, **kwargs):
    """
    Chạy thuật toán BFS trên đồ thị.

    Args:
        graph: Graph object
        start_node: str — đỉnh bắt đầu

    Returns:
        dict chứa 'steps' (list) và 'pseudocode' (list)
    """
    steps = []
    step_num = 0

    visited = set()
    visited_order = []
    queue = deque()
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}

    # Bước 0: Khởi tạo
    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'description': f'Khởi tạo BFS từ đỉnh {start_node}',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Bước 1: Thêm start vào queue
    visited.add(start_node)
    visited_order.append(start_node)
    queue.append(start_node)
    node_colors[start_node] = 'processing'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': list(queue),
        'description': f'Thêm đỉnh {start_node} vào queue và đánh dấu đã thăm',
        'highlight_line': 3,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Vòng lặp BFS
    while queue:
        current = queue.popleft()
        node_colors[current] = 'visited'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': current,
            'current_edge': None,
            'visited': list(visited_order),
            'queue_or_stack': list(queue),
            'description': f'Lấy đỉnh {current} ra khỏi queue, xử lý',
            'highlight_line': 5,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        # Duyệt các đỉnh kề
        neighbors = sorted(graph.get_neighbors(current))
        for neighbor in neighbors:
            edge_key = f"{current}-{neighbor}"
            reverse_key = f"{neighbor}-{current}"

            # Highlight cạnh đang xét
            edge_colors[edge_key] = 'considering'
            if not graph.directed:
                edge_colors[reverse_key] = 'considering'

            if neighbor not in visited:
                visited.add(neighbor)
                visited_order.append(neighbor)
                queue.append(neighbor)
                node_colors[neighbor] = 'processing'

                # Cạnh được chọn
                edge_colors[edge_key] = 'selected'
                if not graph.directed:
                    edge_colors[reverse_key] = 'selected'

                step_num += 1
                steps.append({
                    'step': step_num,
                    'current_node': current,
                    'current_edge': [current, neighbor],
                    'visited': list(visited_order),
                    'queue_or_stack': list(queue),
                    'description': f'Thăm đỉnh {neighbor} (kề {current}), thêm vào queue',
                    'highlight_line': 9,
                    'node_colors': dict(node_colors),
                    'edge_colors': dict(edge_colors),
                    'distances': {},
                })
            else:
                step_num += 1
                steps.append({
                    'step': step_num,
                    'current_node': current,
                    'current_edge': [current, neighbor],
                    'visited': list(visited_order),
                    'queue_or_stack': list(queue),
                    'description': f'Đỉnh {neighbor} đã thăm, bỏ qua',
                    'highlight_line': 8,
                    'node_colors': dict(node_colors),
                    'edge_colors': dict(edge_colors),
                    'distances': {},
                })

    # Bước cuối: hoàn thành
    for node in visited_order:
        node_colors[node] = 'result'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': [],
        'description': f'BFS hoàn thành! Thứ tự duyệt: {" → ".join(visited_order)}',
        'highlight_line': -1,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    return {
        'steps': steps,
        'pseudocode': PSEUDOCODE,
        'result': {
            'traversal_order': visited_order,
            'description': f'Thứ tự duyệt BFS: {" → ".join(visited_order)}'
        }
    }
