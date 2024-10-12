export interface NodeData {
    data: {
        id: string;
        label: string;
    };
}

export interface EdgeData {
    data: {
        source: string;
        target: string;
        label: string;
    };
}

export interface GraphData {
    nodes: NodeData[];
    edges: EdgeData[];
}
