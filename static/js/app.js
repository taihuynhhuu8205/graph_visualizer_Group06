document.addEventListener("DOMContentLoaded", function () {
    const graphDrawer = new GraphDrawer("graphCanvas");

    const verticesInput = document.getElementById("verticesInput");
    const edgesInput = document.getElementById("edgesInput");
    const drawGraphBtn = document.getElementById("drawGraphBtn");
    const clearGraphBtn = document.getElementById("clearGraphBtn");

    drawGraphBtn.addEventListener("click", function () {
        const vertices = parseVertices(verticesInput.value);
        const edges = parseEdges(edgesInput.value);

        if (vertices.length === 0) {
            alert("Vui lòng nhập danh sách đỉnh.");
            return;
        }

        graphDrawer.setGraph(vertices, edges);
    });

    clearGraphBtn.addEventListener("click", function () {
        verticesInput.value = "";
        edgesInput.value = "";
        graphDrawer.clear();
    });
});

function parseVertices(input) {
    return input
        .split(",")
        .map(vertex => vertex.trim())
        .filter(vertex => vertex !== "");
}

function parseEdges(input) {
    return input
        .split(",")
        .map(edge => edge.trim())
        .filter(edge => edge !== "")
        .map(edge => {
            const parts = edge.split("-");

            return {
                from: parts[0]?.trim(),
                to: parts[1]?.trim()
            };
        })
        .filter(edge => edge.from && edge.to);
}