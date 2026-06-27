"""
DFS — Depth-First Search (Duyệt đồ thị theo chiều sâu)

Thuật toán duyệt đồ thị theo chiều sâu sử dụng ngăn xếp (stack).
Trả về danh sách các bước để frontend hiển thị animation.
"""

# Pseudocode cho hiển thị trên frontend
PSEUDOCODE = [
    "DFS(G, start):",
    "  Tạo stack S",
    "  Thêm start vào S",
    "  while S không rỗng:",
    "    u = S.pop()",
    "    if u chưa thăm:",
    "      Đánh dấu u đã thăm",
    "      Xử lý u",
    "      for mỗi v kề u (ngược):",
    "        if v chưa thăm:",
    "          Thêm v vào S",
]


def run(graph, start_node, **kwargs):
    """
    Chạy thuật toán DFS trên đồ thị.

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
    stack = []
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
        'description': f'Khởi tạo DFS từ đỉnh {start_node}',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Thêm start vào stack
    stack.append(start_node)
    node_colors[start_node] = 'processing'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': list(stack),
        'description': f'Thêm đỉnh {start_node} vào stack',
        'highlight_line': 2,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Vòng lặp DFS
    while stack:
        current = stack.pop()

        if current in visited:
            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': current,
                'current_edge': None,
                'visited': list(visited_order),
                'queue_or_stack': list(stack),
                'description': f'Lấy đỉnh {current} ra khỏi stack — đã thăm, bỏ qua',
                'highlight_line': 4,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })
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
            'queue_or_stack': list(stack),
            'description': f'Lấy đỉnh {current} ra khỏi stack, đánh dấu đã thăm',
            'highlight_line': 5,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        # Duyệt các đỉnh kề (ngược thứ tự để duyệt đúng)
        neighbors = sorted(graph.get_neighbors(current), reverse=True)
        for neighbor in neighbors:
            edge_key = f"{current}-{neighbor}"
            reverse_key = f"{neighbor}-{current}"

            edge_colors[edge_key] = 'considering'
            if not graph.directed:
                edge_colors[reverse_key] = 'considering'

            if neighbor not in visited:
                stack.append(neighbor)
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
                    'queue_or_stack': list(stack),
                    'description': f'Thêm đỉnh {neighbor} (kề {current}) vào stack',
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
                    'queue_or_stack': list(stack),
                    'description': f'Đỉnh {neighbor} đã thăm, bỏ qua',
                    'highlight_line': 8,
                    'node_colors': dict(node_colors),
                    'edge_colors': dict(edge_colors),
                    'distances': {},
                })

    # Bước cuối
    for node in visited_order:
        node_colors[node] = 'result'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': list(visited_order),
        'queue_or_stack': [],
        'description': f'DFS hoàn thành! Thứ tự duyệt: {" → ".join(visited_order)}',
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
            'description': f'Thứ tự duyệt DFS: {" → ".join(visited_order)}'
        }
    }
