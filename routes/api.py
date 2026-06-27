
from flask import Blueprint, request, jsonify
from utils.helpers import build_graph_from_json
from algorithms import bfs, dfs, dijkstra, prim, kruskal
from algorithms import ford_fulkerson, fleury, hierholzer, bipartite

api_bp = Blueprint('api', __name__)

# Mapping tên thuật toán → module
ALGORITHMS = {
    'bfs': bfs,
    'dfs': dfs,
    'dijkstra': dijkstra,
    'prim': prim,
    'kruskal': kruskal,
    'ford_fulkerson': ford_fulkerson,
    'fleury': fleury,
    'hierholzer': hierholzer,
    'bipartite': bipartite,
}


@api_bp.route('/run-algorithm', methods=['POST'])
def run_algorithm():

    try:
        data = request.get_json()
        algorithm_name = data.get('algorithm', '').lower()

        if algorithm_name not in ALGORITHMS:
            return jsonify({
                'error': f'Thuật toán "{algorithm_name}" không được hỗ trợ',
                'supported': list(ALGORITHMS.keys())
            }), 400

        # Xây dựng đồ thị
        graph = build_graph_from_json(data)

        if not graph.nodes:
            return jsonify({'error': 'Đồ thị không có đỉnh nào'}), 400

        # Lấy tham số
        params = {}
        if data.get('start_node'):
            params['start_node'] = data['start_node']
        if data.get('end_node'):
            params['end_node'] = data['end_node']

        # Chạy thuật toán
        algo_module = ALGORITHMS[algorithm_name]
        result = algo_module.run(graph, **params)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/convert-representation', methods=['POST'])
def convert_representation():

    try:
        data = request.get_json()
        graph = build_graph_from_json(data)

        return jsonify({
            'adjacency_matrix': graph.to_adjacency_matrix(),
            'adjacency_list': graph.to_adjacency_list(),
            'edge_list': graph.to_edge_list(),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/export-graph', methods=['POST'])
def export_graph():

    try:
        data = request.get_json()
        export_data = {
            'nodes': data.get('nodes', []),
            'edges': data.get('edges', []),
            'directed': data.get('directed', False),
            'weighted': data.get('weighted', False),
        }
        return jsonify(export_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/import-graph', methods=['POST'])
def import_graph():

    try:
        data = request.get_json()

        # Validate
        if 'nodes' not in data or 'edges' not in data:
            return jsonify({'error': 'JSON phải chứa "nodes" và "edges"'}), 400

        # Validate nodes
        for node in data['nodes']:
            if 'id' not in node:
                return jsonify({'error': 'Mỗi node phải có trường "id"'}), 400

        # Validate edges
        node_ids = {n['id'] for n in data['nodes']}
        for edge in data['edges']:
            if 'source' not in edge or 'target' not in edge:
                return jsonify({'error': 'Mỗi edge phải có "source" và "target"'}), 400
            if edge['source'] not in node_ids or edge['target'] not in node_ids:
                return jsonify({'error': f'Edge ({edge["source"]},{edge["target"]}) chứa đỉnh không tồn tại'}), 400

        return jsonify({
            'nodes': data['nodes'],
            'edges': data['edges'],
            'directed': data.get('directed', False),
            'weighted': data.get('weighted', False),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
