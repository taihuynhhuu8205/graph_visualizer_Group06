/**
 * representations.js — Graph Representations
 *
 * Hiển thị adjacency matrix, adjacency list, edge list.
 * Tự động cập nhật khi đồ thị thay đổi.
 */

class RepresentationManager {
    constructor() {
        this.currentRepr = 'matrix';
        this.reprContent = document.getElementById('reprContent');

        this._initEvents();
    }

    /**
     * Khởi tạo event listeners
     */
    _initEvents() {
        document.querySelectorAll('.repr-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const repr = tab.dataset.repr;
                this.setCurrentRepr(repr);
            });
        });
    }

    /**
     * Đặt biểu diễn hiện tại
     */
    setCurrentRepr(repr) {
        this.currentRepr = repr;

        // Update tab UI
        document.querySelectorAll('.repr-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.repr === repr);
        });
    }

    /**
     * Cập nhật biểu diễn từ dữ liệu backend
     */
    update(data) {
        if (!data) {
            this._showPlaceholder();
            return;
        }

        switch (this.currentRepr) {
            case 'matrix':
                this._renderMatrix(data.adjacency_matrix);
                break;
            case 'adjlist':
                this._renderAdjList(data.adjacency_list);
                break;
            case 'edgelist':
                this._renderEdgeList(data.edge_list);
                break;
            default:
                this._showPlaceholder();
        }
    }

    /**
     * Render adjacency matrix
     */
    _renderMatrix(matrixData) {
        if (!matrixData || !matrixData.nodes || matrixData.nodes.length === 0) {
            this._showPlaceholder();
            return;
        }

        const { nodes, matrix } = matrixData;
        let html = '<table class="matrix-table"><tr><th></th>';

        // Header
        nodes.forEach(n => {
            html += `<th>${this._escapeHtml(n)}</th>`;
        });
        html += '</tr>';

        // Rows
        matrix.forEach((row, i) => {
            html += `<tr><th>${this._escapeHtml(nodes[i])}</th>`;
            row.forEach(val => {
                const cls = val !== 0 ? 'nonzero' : '';
                html += `<td class="${cls}">${val}</td>`;
            });
            html += '</tr>';
        });

        html += '</table>';
        this.reprContent.innerHTML = html;
    }

    /**
     * Render adjacency list
     */
    _renderAdjList(adjList) {
        if (!adjList || Object.keys(adjList).length === 0) {
            this._showPlaceholder();
            return;
        }

        let html = '';
        const sortedNodes = Object.keys(adjList).sort();

        sortedNodes.forEach(node => {
            const neighbors = adjList[node];
            let neighborsStr = '';

            if (neighbors.length === 0) {
                neighborsStr = '<span class="text-muted">∅</span>';
            } else {
                neighborsStr = neighbors.map(n => {
                    const weight = n.weight !== 1 ? `<span class="edge-weight">(${n.weight})</span>` : '';
                    return `<span class="neighbor">${this._escapeHtml(n.node)}</span>${weight}`;
                }).join(', ');
            }

            html += `<div class="adj-list-item">
                <span class="node-label">${this._escapeHtml(node)}</span>
                <span class="arrow">→</span>
                ${neighborsStr}
            </div>`;
        });

        this.reprContent.innerHTML = html;
    }

    /**
     * Render edge list
     */
    _renderEdgeList(edgeList) {
        if (!edgeList || edgeList.length === 0) {
            this.reprContent.innerHTML = '<div class="repr-placeholder"><p>Chưa có cạnh nào</p></div>';
            return;
        }

        let html = '';
        edgeList.forEach((edge, idx) => {
            const weightStr = edge.weight !== 1
                ? ` <span class="edge-weight">w=${edge.weight}</span>`
                : '';
            html += `<div class="edge-list-item">
                ${idx + 1}. (${this._escapeHtml(edge.source)}, ${this._escapeHtml(edge.target)})${weightStr}
            </div>`;
        });

        this.reprContent.innerHTML = html;
    }

    /**
     * Hiển thị placeholder
     */
    _showPlaceholder() {
        this.reprContent.innerHTML = `
            <div class="repr-placeholder">
                <i class="fas fa-table"></i>
                <p>Thêm đỉnh và cạnh để xem biểu diễn</p>
            </div>`;
    }

    /**
     * Escape HTML
     */
    _escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
}
