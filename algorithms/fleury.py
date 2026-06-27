"""
Fleury — Thuật toán tìm đường/chu trình Euler

Thuật toán Fleury tìm đường đi hoặc chu trình Euler bằng cách
tại mỗi bước chọn cạnh không phải cầu (bridge) nếu có thể.
"""

# Pseudocode
PSEUDOCODE = [
    "Fleury(G, start):",
    "  path = [start]",
    "  current = start",
    "  while còn cạnh chưa duyệt:",
    "    Lấy danh sách cạnh kề current",
    "    if chỉ có 1 cạnh:",
    "      Chọn cạnh đó",
    "    else:",
    "      Chọn cạnh KHÔNG phải cầu",
    "    Xóa cạnh khỏi đồ thị",
    "    Di chuyển đến đỉnh kế tiếp",
    "    Thêm đỉnh vào path",
    "  return path",
]


def _is_bridge(adj, u, v, nodes):
    """
    Kiểm tra xem cạnh (u, v) có phải là cầu (bridge) không.
    Sử dụng DFS: xóa cạnh, đếm số đỉnh có thể đến từ u.
    """
    # Đếm số đỉnh có thể đến trước khi xóa cạnh
    count_before = _dfs_count(adj, u, nodes)

    # Tạm xóa cạnh
    adj[u].pop(v, None)
    adj[v].pop(u, None)

    # Đếm số đỉnh có thể đến sau khi xóa
    count_after = _dfs_count(adj, u, nodes)

    # Khôi phục cạnh (sẽ được xử lý bên ngoài)
    # Trả về True nếu xóa cạnh làm giảm số đỉnh đạt được
    return count_after < count_before


def _dfs_count(adj, start, nodes):
    """Đếm số đỉnh có thể đến được từ start bằng DFS."""
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in adj.get(node, {}):
                if neighbor not in visited:
                    stack.append(neighbor)
    return len(visited)


def _count_edges(adj):
    """Đếm tổng số cạnh trong đồ thị vô hướng."""
    count = 0
    for u in adj:
        count += len(adj[u])
    return count // 2


def run(graph, start_node=None, **kwargs):
    """
    Chạy thuật toán Fleury tìm đường/chu trình Euler.

    Args:
        graph: Graph object (vô hướng)
        start_node: str hoặc None (tự động chọn)

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}

    # Tạo bản sao adjacency list (sẽ xóa cạnh khi duyệt)
    adj = {}
    for node in graph.nodes:
        adj[node] = dict(graph.adj[node])

    # Kiểm tra điều kiện tồn tại đường/chu trình Euler
    odd_degree_nodes = [n for n in graph.nodes if len(adj[n]) % 2 != 0]

    if len(odd_degree_nodes) > 2:
        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': None,
            'current_edge': None,
            'visited': [],
            'queue_or_stack': [],
            'euler_path': [],
            'description': f'Đồ thị có {len(odd_degree_nodes)} đỉnh bậc lẻ → Không tồn tại đường/chu trình Euler',
            'highlight_line': -1,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })
        return {
            'steps': steps,
            'pseudocode': PSEUDOCODE,
            'result': {
                'euler_path': [],
                'description': 'Không tồn tại đường/chu trình Euler'
            }
        }

    # Chọn đỉnh bắt đầu
    if start_node is None:
        if odd_degree_nodes:
            start_node = odd_degree_nodes[0]
        else:
            # Chọn đỉnh có cạnh
            start_node = graph.nodes[0]
            for n in graph.nodes:
                if len(adj[n]) > 0:
                    start_node = n
                    break

    euler_type = "Chu trình" if len(odd_degree_nodes) == 0 else "Đường đi"

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'euler_path': [start_node],
        'description': f'Khởi tạo Fleury từ đỉnh {start_node}. Tìm {euler_type} Euler',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    path = [start_node]
    current = start_node
    node_colors[current] = 'processing'

    while _count_edges(adj) > 0:
        neighbors = list(adj[current].keys())
        if not neighbors:
            break

        # Chọn cạnh
        chosen_next = None
        if len(neighbors) == 1:
            chosen_next = neighbors[0]
            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': current,
                'current_edge': [current, chosen_next],
                'visited': [],
                'queue_or_stack': [],
                'euler_path': list(path),
                'description': f'Đỉnh {current} chỉ có 1 cạnh kề ({chosen_next}), chọn cạnh này',
                'highlight_line': 5,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })
        else:
            for neighbor in sorted(neighbors):
                # Kiểm tra cầu
                # Lưu trọng số trước khi xóa
                w_uv = adj[current].get(neighbor, 1)
                w_vu = adj[neighbor].get(current, 1)

                # Tạm xóa
                del adj[current][neighbor]
                if current in adj[neighbor]:
                    del adj[neighbor][current]

                bridge = _dfs_count(adj, current, graph.nodes)

                # Khôi phục
                adj[current][neighbor] = w_uv
                adj[neighbor][current] = w_vu

                # Kiểm tra lại
                count_before = _dfs_count(adj, current, graph.nodes)
                del adj[current][neighbor]
                if current in adj[neighbor]:
                    del adj[neighbor][current]
                count_after = _dfs_count(adj, current, graph.nodes)

                # Khôi phục lại
                adj[current][neighbor] = w_uv
                adj[neighbor][current] = w_vu

                is_bridge = count_after < count_before

                if not is_bridge:
                    chosen_next = neighbor
                    step_num += 1
                    steps.append({
                        'step': step_num,
                        'current_node': current,
                        'current_edge': [current, neighbor],
                        'visited': [],
                        'queue_or_stack': [],
                        'euler_path': list(path),
                        'description': f'Cạnh ({current},{neighbor}) không phải cầu → chọn',
                        'highlight_line': 7,
                        'node_colors': dict(node_colors),
                        'edge_colors': dict(edge_colors),
                        'distances': {},
                    })
                    break

            # Nếu tất cả đều là cầu, chọn cạnh đầu tiên
            if chosen_next is None:
                chosen_next = sorted(neighbors)[0]
                step_num += 1
                steps.append({
                    'step': step_num,
                    'current_node': current,
                    'current_edge': [current, chosen_next],
                    'visited': [],
                    'queue_or_stack': [],
                    'euler_path': list(path),
                    'description': f'Tất cả cạnh đều là cầu, buộc chọn ({current},{chosen_next})',
                    'highlight_line': 7,
                    'node_colors': dict(node_colors),
                    'edge_colors': dict(edge_colors),
                    'distances': {},
                })

        # Xóa cạnh và di chuyển
        edge_key = f"{current}-{chosen_next}"
        reverse_key = f"{chosen_next}-{current}"

        adj[current].pop(chosen_next, None)
        adj[chosen_next].pop(current, None)

        edge_colors[edge_key] = 'selected'
        edge_colors[reverse_key] = 'selected'
        node_colors[current] = 'visited'

        current = chosen_next
        path.append(current)
        node_colors[current] = 'processing'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': current,
            'current_edge': None,
            'visited': [],
            'queue_or_stack': [],
            'euler_path': list(path),
            'description': f'Di chuyển đến {current}. Đường đi: {" → ".join(path)}',
            'highlight_line': 10,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

    # Hoàn thành
    for n in path:
        node_colors[n] = 'result'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'euler_path': list(path),
        'description': f'Fleury hoàn thành! {euler_type} Euler: {" → ".join(path)}',
        'highlight_line': 11,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    return {
        'steps': steps,
        'pseudocode': PSEUDOCODE,
        'result': {
            'euler_path': path,
            'description': f'{euler_type} Euler (Fleury): {" → ".join(path)}'
        }
    }
