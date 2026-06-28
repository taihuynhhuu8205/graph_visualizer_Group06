class GraphDrawer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext("2d");
        this.vertices = [];
        this.edges = [];
        this.positions = {};
    }

    setGraph(vertices, edges) {
        this.vertices = vertices;
        this.edges = edges;
        this.calculatePositions();
        this.draw();
    }

    calculatePositions() {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        const radius = 180;
        const totalVertices = this.vertices.length;

        this.vertices.forEach((vertex, index) => {
            const angle = (2 * Math.PI * index) / totalVertices;

            this.positions[vertex] = {
                x: centerX + radius * Math.cos(angle),
                y: centerY + radius * Math.sin(angle)
            };
        });
    }

    clear() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    draw() {
        this.clear();
        this.drawEdges();
        this.drawVertices();
    }

    drawEdges() {
        this.ctx.strokeStyle = "black";
        this.ctx.lineWidth = 2;

        this.edges.forEach(edge => {
            const from = this.positions[edge.from];
            const to = this.positions[edge.to];

            if (!from || !to) {
                return;
            }

            this.ctx.beginPath();
            this.ctx.moveTo(from.x, from.y);
            this.ctx.lineTo(to.x, to.y);
            this.ctx.stroke();
        });
    }

    drawVertices() {
        this.vertices.forEach(vertex => {
            const position = this.positions[vertex];

            this.ctx.beginPath();
            this.ctx.arc(position.x, position.y, 25, 0, 2 * Math.PI);
            this.ctx.fillStyle = "white";
            this.ctx.fill();
            this.ctx.strokeStyle = "black";
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            this.ctx.fillStyle = "black";
            this.ctx.font = "16px Arial";
            this.ctx.textAlign = "center";
            this.ctx.textBaseline = "middle";
            this.ctx.fillText(vertex, position.x, position.y);
        });
    }
}