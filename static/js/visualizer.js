/**
 * visualizer.js — Animation Engine
 *
 * Nhận danh sách steps từ backend, điều khiển animation:
 * Play/Pause/Next/Previous/Reset, tốc độ, tô màu node/edge.
 */

class Visualizer {
    constructor(graphManager) {
        this.graph = graphManager;
        this.steps = [];
        this.pseudocode = [];
        this.currentStep = -1;
        this.isPlaying = false;
        this.speed = 1;  // Tốc độ mặc định 1x
        this.animationTimer = null;
        this.result = null;

        // DOM elements
        this.controls = document.getElementById('animationControls');
        this.stepCounter = document.getElementById('stepCounter');
        this.progressBar = document.getElementById('progressBarFill');
        this.playPauseIcon = document.getElementById('playPauseIcon');
        this.pseudocodeContainer = document.getElementById('pseudocodeContainer');
        this.stepDescription = document.getElementById('stepDescription');
        this.queueStackSection = document.getElementById('queueStackSection');
        this.queueStackLabel = document.getElementById('queueStackLabel');
        this.queueStackContainer = document.getElementById('queueStackContainer');
        this.visitedSection = document.getElementById('visitedSection');
        this.visitedContainer = document.getElementById('visitedContainer');
        this.distancesSection = document.getElementById('distancesSection');
        this.distancesContainer = document.getElementById('distancesContainer');
        this.resultContainer = document.getElementById('resultContainer');
    }

    /**
     * Tải kết quả từ backend và bắt đầu animation
     */
    loadResult(data, algorithmName) {
        this.steps = data.steps || [];
        this.pseudocode = data.pseudocode || [];
        this.result = data.result || {};
        this.currentStep = -1;
        this.isPlaying = false;
        this.algorithmName = algorithmName;

        // Hiển thị controls
        this.controls.style.display = 'block';

        // Hiển thị pseudocode
        this._renderPseudocode();

        // Hiển thị sections dựa trên thuật toán
        this._showRelevantSections(algorithmName);

        // Hiển thị kết quả cuối
        this._renderResult();

        // Reset về bước 0
        this.reset();

        // Tự động chuyển đến bước đầu
        this.nextStep();
    }

    /**
     * Play/Pause toggle
     */
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    /**
     * Play animation
     */
    play() {
        if (this.currentStep >= this.steps.length - 1) {
            // Nếu đã hết, reset và play lại
            this.reset();
        }
        this.isPlaying = true;
        this.playPauseIcon.className = 'fas fa-pause';
        this._scheduleNext();
    }

    /**
     * Pause animation
     */
    pause() {
        this.isPlaying = false;
        this.playPauseIcon.className = 'fas fa-play';
        if (this.animationTimer) {
            clearTimeout(this.animationTimer);
            this.animationTimer = null;
        }
    }

    /**
     * Bước tiếp theo
     */
    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this._applyStep(this.currentStep);
        } else {
            this.pause();
        }
    }

    /**
     * Bước trước
     */
    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this._applyStep(this.currentStep);
        }
    }

    /**
     * Reset về đầu
     */
    reset() {
        this.pause();
        this.currentStep = -1;
        this.graph.resetVisuals();
        this._updateStepCounter();
        this._updateProgress();
        this._clearStepInfo();
        this._highlightPseudocodeLine(-1);
    }

    /**
     * Đặt tốc độ
     */
    setSpeed(speed) {
        this.speed = speed;
    }

    /**
     * Apply step hiện tại lên đồ thị
     */
    _applyStep(stepIndex) {
        const step = this.steps[stepIndex];
        if (!step) return;

        // Reset visual trước
        this.graph.resetVisuals();

        // Apply node colors
        if (step.node_colors) {
            for (const [nodeId, colorClass] of Object.entries(step.node_colors)) {
                this.graph.setNodeColor(nodeId, colorClass);
            }
        }

        // Apply edge colors
        if (step.edge_colors) {
            for (const [edgeId, colorClass] of Object.entries(step.edge_colors)) {
                this.graph.setEdgeColor(edgeId, colorClass);
            }
        }

        // Update UI
        this._updateStepCounter();
        this._updateProgress();
        this._updateStepDescription(step);
        this._updateQueueStack(step);
        this._updateVisited(step);
        this._updateDistances(step);
        this._highlightPseudocodeLine(step.highlight_line);

        // Schedule next step if playing
        if (this.isPlaying) {
            this._scheduleNext();
        }
    }

    /**
     * Lên lịch bước tiếp theo
     */
    _scheduleNext() {
        if (this.animationTimer) {
            clearTimeout(this.animationTimer);
        }
        const delay = 1000 / this.speed;
        this.animationTimer = setTimeout(() => {
            this.nextStep();
        }, delay);
    }

    /**
     * Render pseudocode
     */
    _renderPseudocode() {
        if (this.pseudocode.length === 0) {
            this.pseudocodeContainer.innerHTML = `
                <div class="pseudocode-placeholder">
                    <i class="fas fa-play-circle"></i>
                    <p>Không có pseudocode</p>
                </div>`;
            return;
        }

        let html = '';
        this.pseudocode.forEach((line, idx) => {
            html += `<div class="pseudo-line" data-line="${idx}">${this._escapeHtml(line)}</div>`;
        });
        this.pseudocodeContainer.innerHTML = html;
    }

    /**
     * Highlight dòng pseudocode
     */
    _highlightPseudocodeLine(lineIndex) {
        const lines = this.pseudocodeContainer.querySelectorAll('.pseudo-line');
        lines.forEach(line => line.classList.remove('active'));

        if (lineIndex >= 0 && lineIndex < lines.length) {
            lines[lineIndex].classList.add('active');
            // Scroll vào view
            lines[lineIndex].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
    }

    /**
     * Cập nhật step counter
     */
    _updateStepCounter() {
        const current = this.currentStep >= 0 ? this.currentStep + 1 : 0;
        this.stepCounter.textContent = `Bước ${current} / ${this.steps.length}`;
    }

    /**
     * Cập nhật progress bar
     */
    _updateProgress() {
        const progress = this.steps.length > 0
            ? ((this.currentStep + 1) / this.steps.length) * 100
            : 0;
        this.progressBar.style.width = `${progress}%`;
    }

    /**
     * Cập nhật mô tả bước
     */
    _updateStepDescription(step) {
        this.stepDescription.innerHTML = `<p class="step-desc-text">${this._escapeHtml(step.description)}</p>`;
    }

    /**
     * Cập nhật Queue/Stack
     */
    _updateQueueStack(step) {
        if (!step.queue_or_stack || step.queue_or_stack.length === 0) {
            this.queueStackContainer.innerHTML = '<span class="text-muted">Trống</span>';
            return;
        }

        let html = '';
        step.queue_or_stack.forEach((item, idx) => {
            const isLast = idx === step.queue_or_stack.length - 1;
            html += `<span class="data-badge ${isLast ? 'current' : ''}">${this._escapeHtml(String(item))}</span>`;
        });
        this.queueStackContainer.innerHTML = html;
    }

    /**
     * Cập nhật danh sách đã duyệt
     */
    _updateVisited(step) {
        if (!step.visited || step.visited.length === 0) {
            this.visitedContainer.innerHTML = '<span class="text-muted">Trống</span>';
            return;
        }

        let html = '';
        step.visited.forEach(item => {
            html += `<span class="data-badge visited">${this._escapeHtml(String(item))}</span>`;
        });
        this.visitedContainer.innerHTML = html;
    }

    /**
     * Cập nhật bảng khoảng cách
     */
    _updateDistances(step) {
        if (!step.distances || Object.keys(step.distances).length === 0) {
            this.distancesContainer.innerHTML = '<span class="text-muted">Trống</span>';
            return;
        }

        let html = '<table class="dist-table"><tr><th>Đỉnh</th><th>Khoảng cách</th></tr>';
        const sorted = Object.entries(step.distances).sort(([a], [b]) => a.localeCompare(b));
        for (const [node, dist] of sorted) {
            const cls = dist !== '∞' ? 'updated' : '';
            html += `<tr><td>${this._escapeHtml(node)}</td><td class="${cls}">${dist}</td></tr>`;
        }
        html += '</table>';
        this.distancesContainer.innerHTML = html;
    }

    /**
     * Hiển thị kết quả cuối cùng
     */
    _renderResult() {
        if (!this.result || !this.result.description) {
            this.resultContainer.innerHTML = '<p class="text-muted">Chạy thuật toán để xem kết quả</p>';
            return;
        }

        let html = `<p class="result-text">${this._escapeHtml(this.result.description)}</p>`;

        if (this.result.total_weight !== undefined && this.result.total_weight !== null) {
            html += `<p>Tổng trọng số: <span class="result-value">${this.result.total_weight}</span></p>`;
        }
        if (this.result.max_flow !== undefined && this.result.max_flow !== null) {
            html += `<p>Max Flow: <span class="result-value">${this.result.max_flow}</span></p>`;
        }
        if (this.result.path && this.result.path.length > 0) {
            html += `<p>Đường đi: <span class="result-value">${this.result.path.join(' → ')}</span></p>`;
        }
        if (this.result.euler_path && this.result.euler_path.length > 0) {
            html += `<p>Chu trình Euler: <span class="result-value">${this.result.euler_path.join(' → ')}</span></p>`;
        }
        if (this.result.is_bipartite !== undefined) {
            if (this.result.is_bipartite) {
                html += `<p>Tập A: <span class="result-value">{${(this.result.set_a || []).join(', ')}}</span></p>`;
                html += `<p>Tập B: <span class="result-value">{${(this.result.set_b || []).join(', ')}}</span></p>`;
            }
        }

        this.resultContainer.innerHTML = html;
    }

    /**
     * Hiển thị/ẩn sections tùy theo thuật toán
     */
    _showRelevantSections(algoName) {
        const showQS = ['bfs', 'dfs', 'dijkstra', 'prim', 'hierholzer'].includes(algoName);
        const showVisited = ['bfs', 'dfs', 'dijkstra', 'prim', 'bipartite'].includes(algoName);
        const showDist = ['dijkstra'].includes(algoName);

        this.queueStackSection.style.display = showQS ? 'block' : 'none';
        this.visitedSection.style.display = showVisited ? 'block' : 'none';
        this.distancesSection.style.display = showDist ? 'block' : 'none';

        // Label
        if (algoName === 'bfs') {
            this.queueStackLabel.textContent = 'Queue';
        } else if (algoName === 'dfs') {
            this.queueStackLabel.textContent = 'Stack';
        } else if (algoName === 'hierholzer') {
            this.queueStackLabel.textContent = 'Stack';
        } else {
            this.queueStackLabel.textContent = 'Priority Queue';
        }
    }

    /**
     * Xóa thông tin bước
     */
    _clearStepInfo() {
        this.stepDescription.innerHTML = '<p class="text-muted">Chưa có thông tin</p>';
        this.queueStackContainer.innerHTML = '<span class="text-muted">Trống</span>';
        this.visitedContainer.innerHTML = '<span class="text-muted">Trống</span>';
        this.distancesContainer.innerHTML = '<span class="text-muted">Trống</span>';
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
