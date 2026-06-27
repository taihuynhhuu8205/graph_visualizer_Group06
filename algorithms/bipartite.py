"""
Bipartite Check — Kiểm tra đồ thị hai phía

Sử dụng BFS để kiểm tra xem đồ thị có phải là đồ thị hai phía (bipartite) không.
Nếu có, trả về phân hoạch hai tập đỉnh.
"""
from collections import deque

# Pseudocode
PSEUDOCODE = [
    "BipartiteCheck(G):",
    "  color = {} (chưa tô màu)",
    "  for mỗi đỉnh v chưa tô:",
    "    color[v] = 0",
    "    queue Q = [v]",
    "    while Q không rỗng:",
    "      u = Q.dequeue()",
    "      for mỗi w kề u:",
    "        if w chưa tô:",
    "          color[w] = 1 - color[u]",
    "          Q.enqueue(w)",
    "        else if color[w] == color[u]:",
    "          return False (không 2 phía)",
    "  return True, partition",
]


def run(graph, **kwargs):
    """
    Kiểm tra đồ thị có phải là đồ thị hai phía không.

    Args:
        graph: Graph object

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}
    partition = {}  # node -> 0 hoặc 1
    is_bipartite = True
    conflict_edge = None

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'partition': {},
        'description': 'Khởi tạo kiểm tra đồ thị hai phía (Bipartite Check)',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    for start in graph.nodes:
        if start in partition:
            continue

        # BFS từ đỉnh chưa tô
        partition[start] = 0
        queue = deque([start])
        node_colors[start] = 'processing'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': start,
            'current_edge': None,
            'visited': list(partition.keys()),
            'queue_or_stack': list(queue),
            'partition': dict(partition),
            'description': f'Bắt đầu BFS từ đỉnh {start}, tô màu 0 (Tập A)',
            'highlight_line': 3,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        while queue and is_bipartite:
            current = queue.popleft()
            current_color = partition[current]
            node_colors[current] = 'visited'

            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': current,
                'current_edge': None,
                'visited': list(partition.keys()),
                'queue_or_stack': list(queue),
                'partition': dict(partition),
                'description': f'Xử lý đỉnh {current} (Tập {"A" if current_color == 0 else "B"})',
                'highlight_line': 6,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })

            for neighbor in sorted(graph.get_neighbors(current)):
                edge_key = f"{current}-{neighbor}"
                reverse_key = f"{neighbor}-{current}"
                edge_colors[edge_key] = 'considering'
                if not graph.directed:
                    edge_colors[reverse_key] = 'considering'

                if neighbor not in partition:
                    partition[neighbor] = 1 - current_color
                    queue.append(neighbor)
                    node_colors[neighbor] = 'processing'
                    edge_colors[edge_key] = 'selected'
                    if not graph.directed:
                        edge_colors[reverse_key] = 'selected'

                    step_num += 1
                    steps.append({
                        'step': step_num,
                        'current_node': current,
                        'current_edge': [current, neighbor],
                        'visited': list(partition.keys()),
                        'queue_or_stack': list(queue),
                        'partition': dict(partition),
                        'description': f'Tô {neighbor} màu {1 - current_color} (Tập {"B" if current_color == 0 else "A"})',
                        'highlight_line': 9,
                        'node_colors': dict(node_colors),
                        'edge_colors': dict(edge_colors),
                        'distances': {},
                    })
                elif partition[neighbor] == current_color:
                    # Xung đột — không phải bipartite
                    is_bipartite = False
                    conflict_edge = [current, neighbor]

                    node_colors[current] = 'result'
                    node_colors[neighbor] = 'result'

                    step_num += 1
                    steps.append({
                        'step': step_num,
                        'current_node': current,
                        'current_edge': [current, neighbor],
                        'visited': list(partition.keys()),
                        'queue_or_stack': list(queue),
                        'partition': dict(partition),
                        'description': f'Xung đột! {current} và {neighbor} cùng tập → Đồ thị KHÔNG phải hai phía',
                        'highlight_line': 12,
                        'node_colors': dict(node_colors),
                        'edge_colors': dict(edge_colors),
                        'distances': {},
                    })
                    break

        if not is_bipartite:
            break

    # Kết quả cuối cùng
    if is_bipartite:
        set_a = sorted([n for n, c in partition.items() if c == 0])
        set_b = sorted([n for n, c in partition.items() if c == 1])

        for n in set_a:
            node_colors[n] = 'result'
        for n in set_b:
            node_colors[n] = 'visited'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': None,
            'current_edge': None,
            'visited': list(partition.keys()),
            'queue_or_stack': [],
            'partition': dict(partition),
            'description': f'Đồ thị HAI PHÍA! Tập A: {{{", ".join(set_a)}}} | Tập B: {{{", ".join(set_b)}}}',
            'highlight_line': 13,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        return {
            'steps': steps,
            'pseudocode': PSEUDOCODE,
            'result': {
                'is_bipartite': True,
                'partition': partition,
                'set_a': set_a,
                'set_b': set_b,
                'description': f'Đồ thị hai phía. Tập A: {{{", ".join(set_a)}}} | Tập B: {{{", ".join(set_b)}}}'
            }
        }
    else:
        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': None,
            'current_edge': None,
            'visited': list(partition.keys()),
            'queue_or_stack': [],
            'partition': dict(partition),
            'description': f'Kết luận: Đồ thị KHÔNG phải hai phía (xung đột tại cạnh {conflict_edge})',
            'highlight_line': 12,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        return {
            'steps': steps,
            'pseudocode': PSEUDOCODE,
            'result': {
                'is_bipartite': False,
                'conflict_edge': conflict_edge,
                'description': f'Đồ thị KHÔNG phải hai phía'
            }
        }
