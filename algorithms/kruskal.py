"""
Kruskal — Thuật toán tìm cây khung nhỏ nhất (Minimum Spanning Tree)

Thuật toán Kruskal sắp xếp tất cả cạnh theo trọng số tăng dần,
sau đó thêm từng cạnh vào MST nếu không tạo chu trình (sử dụng Union-Find).
"""

# Pseudocode
PSEUDOCODE = [
    "Kruskal(G):",
    "  Sắp xếp cạnh theo trọng số tăng dần",
    "  MST = ∅, totalWeight = 0",
    "  Khởi tạo Union-Find",
    "  for mỗi cạnh (u, v, w):",
    "    if Find(u) ≠ Find(v):",
    "      MST = MST ∪ {(u, v, w)}",
    "      Union(u, v)",
    "      totalWeight += w",
    "    else:",
    "      Bỏ qua (tạo chu trình)",
    "  return MST, totalWeight",
]


class UnionFind:
    """Cấu trúc dữ liệu Union-Find (Disjoint Set Union)."""

    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, x):
        """Tìm đại diện của tập chứa x (có path compression)."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Hợp nhất hai tập chứa x và y (union by rank)."""
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        return True


def run(graph, **kwargs):
    """
    Chạy thuật toán Kruskal tìm MST.

    Args:
        graph: Graph object

    Returns:
        dict chứa 'steps', 'pseudocode', 'result'
    """
    steps = []
    step_num = 0
    mst_edges = []
    total_weight = 0
    node_colors = {n: 'default' for n in graph.nodes}
    edge_colors = {}

    # Lấy tất cả cạnh và sắp xếp theo trọng số
    all_edges = graph.get_all_edges()
    all_edges.sort(key=lambda e: e[2])

    # Khởi tạo Union-Find
    uf = UnionFind(graph.nodes)

    step_num += 1
    edge_list_str = ', '.join([f"({s},{t},{w})" for s, t, w in all_edges])
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'mst_edges': [],
        'total_weight': 0,
        'description': f'Sắp xếp {len(all_edges)} cạnh theo trọng số: {edge_list_str}',
        'highlight_line': 1,
        'node_colors': dict(node_colors),
        'edge_colors': dict(edge_colors),
        'distances': {},
    })

    # Duyệt từng cạnh
    for source, target, weight in all_edges:
        edge_key = f"{source}-{target}"
        reverse_key = f"{target}-{source}"

        edge_colors[edge_key] = 'considering'
        if not graph.directed:
            edge_colors[reverse_key] = 'considering'

        step_num += 1
        steps.append({
            'step': step_num,
            'current_node': None,
            'current_edge': [source, target],
            'visited': [],
            'queue_or_stack': [],
            'mst_edges': list(mst_edges),
            'total_weight': total_weight,
            'description': f'Xét cạnh ({source},{target},w={weight})',
            'highlight_line': 4,
            'node_colors': dict(node_colors),
            'edge_colors': dict(edge_colors),
            'distances': {},
        })

        if uf.find(source) != uf.find(target):
            # Không tạo chu trình → thêm vào MST
            uf.union(source, target)
            mst_edges.append([source, target, weight])
            total_weight += weight

            node_colors[source] = 'visited'
            node_colors[target] = 'visited'
            edge_colors[edge_key] = 'selected'
            if not graph.directed:
                edge_colors[reverse_key] = 'selected'

            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': None,
                'current_edge': [source, target],
                'visited': [],
                'queue_or_stack': [],
                'mst_edges': list(mst_edges),
                'total_weight': total_weight,
                'description': f'Thêm cạnh ({source},{target},w={weight}) vào MST. Tổng = {total_weight}',
                'highlight_line': 6,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })
        else:
            # Tạo chu trình → bỏ qua
            step_num += 1
            steps.append({
                'step': step_num,
                'current_node': None,
                'current_edge': [source, target],
                'visited': [],
                'queue_or_stack': [],
                'mst_edges': list(mst_edges),
                'total_weight': total_weight,
                'description': f'Cạnh ({source},{target},w={weight}) tạo chu trình, bỏ qua',
                'highlight_line': 10,
                'node_colors': dict(node_colors),
                'edge_colors': dict(edge_colors),
                'distances': {},
            })

        # Dừng sớm nếu đã có đủ cạnh
        if len(mst_edges) == len(graph.nodes) - 1:
            break

    # Hoàn thành
    for edge in mst_edges:
        node_colors[edge[0]] = 'result'
        node_colors[edge[1]] = 'result'

    step_num += 1
    mst_desc = ', '.join([f"({s},{t},w={w})" for s, t, w in mst_edges])
    steps.append({
        'step': step_num,
        'current_node': None,
        'current_edge': None,
        'visited': [],
        'queue_or_stack': [],
        'mst_edges': list(mst_edges),
        'total_weight': total_weight,
        'description': f'Kruskal hoàn thành! MST: {mst_desc}. Tổng trọng số = {total_weight}',
        'highlight_line': 11,
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
            'description': f'MST (Kruskal): tổng trọng số = {total_weight}'
        }
    }
