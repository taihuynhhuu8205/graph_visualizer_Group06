"""
Hierholzer — Thuật toán tìm chu trình/đường đi Euler

Thuật toán Hierholzer hiệu quả hơn Fleury, sử dụng stack
để xây dựng chu trình Euler bằng cách tìm các chu trình con.
"""

# Pseudocode
PSEUDOCODE = [
    "Hierholzer(G, start):",
    "  stack = [start]",
    "  circuit = []",
    "  while stack không rỗng:",
    "    v = stack.top()",
    "    if v còn cạnh kề:",
    "      u = đỉnh kề v",
    "      Xóa cạnh (v, u)",
    "      stack.push(u)",
    "    else:",
    "      stack.pop()",
    "      circuit.prepend(v)",
    "  return circuit",
]


def run(graph, start_node=None, **kwargs):
    """
    Chạy thuật toán Hierholzer tìm chu trình/đường đi Euler.

    Args:
        graph: Graph object
        start_node: str hoặc None (tự động chọn)

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}

    # Tạo bản sao adjacency list
    adj = {}
    for node in graph.nodes:
        adj[node] = dict(graph.adj[node])

    # Kiểm tra điều kiện
    if graph.directed:
        # Đồ thị có hướng: kiểm tra in-degree == out-degree
        imbalance = []
        for node in graph.nodes:
            in_deg = sum(1 for n in graph.nodes if node in graph.adj.get(n, {}))
            out_deg = len(graph.adj.get(node, {}))
            if in_deg != out_deg:
                imbalance.append((node, in_deg, out_deg))

        if len(imbalance) > 2:
            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': None,
                'current_edge': None,
                'visited': [],
                'queue_or_stack': [],
                'euler_path': [],
                'description': 'Đồ thị có hướng không thỏa điều kiện Euler',
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
    else:
        # Đồ thị vô hướng: kiểm tra bậc lẻ
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
        if not graph.directed:
            odd_nodes = [n for n in graph.nodes if len(adj[n]) % 2 != 0]
            if odd_nodes:
                start_node = odd_nodes[0]
            else:
                start_node = graph.nodes[0]
                for n in graph.nodes:
                    if len(adj[n]) > 0:
                        start_node = n
                        break
        else:
            start_node = graph.nodes[0]

    euler_type = "Chu trình" if all(len(adj[n]) % 2 == 0 for n in graph.nodes) else "Đường đi"

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': start_node,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [start_node],
        'euler_path': [],
        'description': f'Khởi tạo Hierholzer từ đỉnh {start_node}. Tìm {euler_type} Euler',
        'highlight_line': 0,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Thuật toán Hierholzer
    stack = [start_node]
    circuit = []

    while stack:
        v = stack[-1]
        node_colors[v] = 'processing'

        if adj[v]:  # Còn cạnh kề
            u = sorted(adj[v].keys())[0]  # Chọn đỉnh kề đầu tiên

            edge_key = f"{v}-{u}"
            reverse_key = f"{u}-{v}"

            # Xóa cạnh
            del adj[v][u]
            if not graph.directed and u in adj and v in adj[u]:
                del adj[u][v]

            edge_colors[edge_key] = 'selected'
            if not graph.directed:
                edge_colors[reverse_key] = 'selected'

            stack.append(u)

            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': v,
                'current_edge': [v, u],
                'visited': [],
                'queue_or_stack': list(stack),
                'euler_path': list(circuit),
                'description': f'Đi từ {v} đến {u}, xóa cạnh ({v},{u}). Stack: {stack}',
                'highlight_line': 7,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })
        else:
            # Không còn cạnh kề → pop và thêm vào circuit
            stack.pop()
            circuit.insert(0, v)
            node_colors[v] = 'visited'

            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': v,
                'current_edge': None,
                'visited': [],
                'queue_or_stack': list(stack),
                'euler_path': list(circuit),
                'description': f'Đỉnh {v} không còn cạnh kề, thêm vào circuit: {" → ".join(circuit)}',
                'highlight_line': 10,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })

    # Hoàn thành
    for n in circuit:
        node_colors[n] = 'result'

    step_num += 1
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'euler_path': list(circuit),
        'description': f'Hierholzer hoàn thành! {euler_type} Euler: {" → ".join(circuit)}',
        'highlight_line': 11,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    return {
        'steps': steps,
        'pseudocode': PSEUDOCODE,
        'result': {
            'euler_path': circuit,
            'description': f'{euler_type} Euler (Hierholzer): {" → ".join(circuit)}'
        }
    }
