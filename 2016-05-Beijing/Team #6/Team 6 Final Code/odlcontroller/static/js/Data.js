var topologyData = {
    nodes: [
        {"id": 0, "x": 150, "y": 300, "name": "por"},
        {"id": 1, "x": 350, "y": 300, "name": "sfc"},
        {"id": 2, "x": 300, "y": 175, "name": "sea"},
        {"id": 3, "x": 500, "y": 175, "name": "sjc"},
        {"id": 4, "x": 450, "y": 50, "name": "min"},
        {"id": 5, "x": 700, "y": 175, "name": "lax"},
        {"id": 6, "x": 650, "y": 50, "name": "kcy"},
        {"id": 7, "x": 850, "y": 100, "name": "san"},
    ],
    links: [
        {"source": 0, "target": 1, id: 0},
        {"source": 0, "target": 2, id: 1},
        {"source": 1, "target": 3, id: 2},
        {"source": 2, "target": 3, id: 3},
        {"source": 2, "target": 4, id: 4},
        {"source": 3, "target": 4, id: 5},
        {"source": 4, "target": 6, id: 6},
        {"source": 3, "target": 6, id: 7},
        {"source": 3, "target": 5, id: 8},
        {"source": 5, "target": 6, id: 9},
        {"source": 5, "target": 7, id: 10},
        {"source": 6, "target": 7, id: 11}
    ]
};

