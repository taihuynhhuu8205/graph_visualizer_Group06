/**
 * sidebar.js — Sidebar Controls
 *
 * Xử lý tương tác sidebar: chọn thuật toán, chế độ vẽ,
 * hiển thị form tham số phù hợp.
 */

class SidebarManager {
    constructor() {
        // DOM elements
        this.algorithmSelect = document.getElementById('algorithmSelect');
        this.algoParams = document.getElementById('algoParams');
        this.startNodeGroup = document.getElementById('startNodeGroup');
        this.endNodeGroup = document.getElementById('endNodeGroup');
        this.startNodeSelect = document.getElementById('startNodeSelect');
        this.endNodeSelect = document.getElementById('endNodeSelect');

        // Chế độ vẽ hiện tại
        this.currentMode = 'addNode';

        // Thuật toán cần start node
        this.needsStartNode = ['bfs', 'dfs', 'dijkstra', 'prim', 'fleury', 'hierholzer'];
        this.needsEndNode = ['dijkstra', 'ford_fulkerson'];
        this.needsSource = ['ford_fulkerson'];

        this._initEvents();
    }

    /**
     * Khởi tạo event listeners
     */
    _initEvents() {
        // Algorithm change
        this.algorithmSelect.addEventListener('change', () => {
            this._onAlgorithmChange();
        });
    }

    /**
     * Khi chọn thuật toán
     */
    _onAlgorithmChange() {
        const algo = this.algorithmSelect.value;

        if (!algo) {
            this.algoParams.style.display = 'none';
            return;
        }

        this.algoParams.style.display = 'block';

        // Hiển thị/ẩn start node
        if (this.needsStartNode.includes(algo) || this.needsSource.includes(algo)) {
            this.startNodeGroup.style.display = 'block';
            // Đổi label cho Ford-Fulkerson
            const label = this.startNodeGroup.querySelector('label');
            if (this.needsSource.includes(algo)) {
                label.textContent = 'Source';
            } else {
                label.textContent = 'Đỉnh bắt đầu';
            }
        } else {
            this.startNodeGroup.style.display = 'none';
        }

        // Hiển thị/ẩn end node
        if (this.needsEndNode.includes(algo)) {
            this.endNodeGroup.style.display = 'block';
            const label = this.endNodeGroup.querySelector('label');
            if (this.needsSource.includes(algo)) {
                label.textContent = 'Sink';
            } else {
                label.textContent = 'Đỉnh kết thúc';
            }
        } else {
            this.endNodeGroup.style.display = 'none';
        }
    }

    /**
     * Cập nhật danh sách node cho select boxes
     */
    updateNodeSelects(nodeIds) {
        const updateSelect = (select) => {
            const currentValue = select.value;
            select.innerHTML = '<option value="">Chọn đỉnh...</option>';
            nodeIds.forEach(id => {
                const option = document.createElement('option');
                option.value = id;
                option.textContent = id;
                select.appendChild(option);
            });
            // Khôi phục selection nếu còn tồn tại
            if (nodeIds.includes(currentValue)) {
                select.value = currentValue;
            }
        };

        updateSelect(this.startNodeSelect);
        updateSelect(this.endNodeSelect);
    }

    /**
     * Lấy tham số thuật toán hiện tại
     */
    getAlgorithmParams() {
        return {
            algorithm: this.algorithmSelect.value,
            start_node: this.startNodeSelect.value || null,
            end_node: this.endNodeSelect.value || null,
        };
    }

    /**
     * Set draw mode
     */
    setDrawMode(mode) {
        this.currentMode = mode;

        // Update button UI
        document.querySelectorAll('.btn-mode').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        // Update toolbar label
        const labels = {
            addNode: { icon: 'fa-circle-plus', text: 'Thêm đỉnh', hint: 'Click vào canvas để thêm đỉnh' },
            addEdge: { icon: 'fa-link', text: 'Thêm cạnh', hint: 'Click 2 đỉnh liên tiếp để tạo cạnh' },
            delete: { icon: 'fa-eraser', text: 'Xóa', hint: 'Click vào đỉnh hoặc cạnh để xóa' },
            move: { icon: 'fa-arrows-alt', text: 'Di chuyển', hint: 'Kéo thả đỉnh để di chuyển' },
        };

        const label = labels[mode] || labels.addNode;
        document.getElementById('currentModeLabel').innerHTML =
            `<i class="fas ${label.icon}"></i> ${label.text}`;
        document.getElementById('modeHint').textContent = label.hint;
    }

    /**
     * Lấy chế độ vẽ hiện tại
     */
    getDrawMode() {
        return this.currentMode;
    }
}
