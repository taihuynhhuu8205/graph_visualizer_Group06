
class Graph:


    def __init__(self, nodes, edges, directed=False, weighted=False):

        self.nodes = list(nodes)
        self.edges = list(edges)
        self.directed = directed
        self.weighted = weighted
        self.adj = {}  # Adjacency list: {node: {neighbor: weight}}

        # Khởi tạo adjacency list rỗng cho mỗi đỉnh
        for node in self.nodes:
            self.adj[node] = {}

        # Thêm cạnh vào adjacency list
        for edge in self.edges:
            source = edge['source']
            target = edge['target']
            weight = edge.get('weight', 1)

            self.adj[source][target] = weight
            if not self.directed:
                self.adj[target][source] = weight

    def get_neighbors(self, node):
        """Trả về danh sách các đỉnh kề của node."""
        return list(self.adj.get(node, {}).keys())

    def get_weight(self, source, target):
        """Trả về trọng số cạnh (source, target). Mặc định 1 nếu không có trọng số."""
        return self.adj.get(source, {}).get(target, float('inf'))

    def has_edge(self, source, target):
        """Kiểm tra xem có cạnh (source, target) không."""
        return target in self.adj.get(source, {})

    def get_edge_weight(self, source, target):
        """Trả về trọng số cạnh, hoặc None nếu cạnh không tồn tại."""
        if self.has_edge(source, target):
            return self.adj[source][target]
        return None

    def get_all_edges(self):

        edges = []
        visited_edges = set()
        for source in self.nodes:
            for target, weight in self.adj[source].items():
                if self.directed:
                    edges.append((source, target, weight))
                else:
                    edge_key = tuple(sorted([source, target]))
                    if edge_key not in visited_edges:
                        visited_edges.add(edge_key)
                        edges.append((source, target, weight))
        return edges

    def get_degree(self, node):
        """Trả về bậc (degree) của đỉnh."""
        if self.directed:
            # In-degree + out-degree
            in_degree = sum(1 for n in self.nodes if node in self.adj.get(n, {}))
            out_degree = len(self.adj.get(node, {}))
            return in_degree + out_degree
        return len(self.adj.get(node, {}))

    def get_in_degree(self, node):
        """Trả về bậc vào (in-degree) cho đồ thị có hướng."""
        return sum(1 for n in self.nodes if node in self.adj.get(n, {}))

    def get_out_degree(self, node):
        """Trả về bậc ra (out-degree) cho đồ thị có hướng."""
        return len(self.adj.get(node, {}))

    def to_adjacency_matrix(self):

        n = len(self.nodes)
        node_index = {node: i for i, node in enumerate(self.nodes)}
        matrix = [[0] * n for _ in range(n)]

        for source in self.nodes:
            for target, weight in self.adj[source].items():
                i = node_index[source]
                j = node_index[target]
                matrix[i][j] = weight

        return {
            'nodes': self.nodes,
            'matrix': matrix
        }

    def to_adjacency_list(self):

        result = {}
        for node in self.nodes:
            result[node] = [
                {'node': neighbor, 'weight': weight}
                for neighbor, weight in sorted(self.adj[node].items())
            ]
        return result

    def to_edge_list(self):

        edges = self.get_all_edges()
        return [
            {'source': s, 'target': t, 'weight': w}
            for s, t, w in edges
        ]

    def node_count(self):
        """Trả về số đỉnh."""
        return len(self.nodes)

    def edge_count(self):
        """Trả về số cạnh."""
        return len(self.get_all_edges())

    def copy(self):
        """Tạo bản sao của đồ thị."""
        return Graph(
            list(self.nodes),
            [dict(e) for e in self.edges],
            self.directed,
            self.weighted
        )
