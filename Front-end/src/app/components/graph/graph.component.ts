import { Component, OnInit } from '@angular/core';
import { GraphService } from '../../services/graph/graph.service';
import cytoscape from 'cytoscape';
import { NodeData, EdgeData, GraphData } from '../../interfaces/graph.interfaces';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  private cy!: cytoscape.Core; // Use definite assignment assertion

  constructor(private graphService: GraphService) {}

  ngOnInit(): void {
    this.graphService.getGraphData().subscribe(data => {
      this.initializeGraph(data);
    });
  }

  initializeGraph(data: GraphData): void {
    const elements = [
      ...data.nodes.map((node: NodeData) => ({
        data: node.data
      })),
      ...data.edges.map((edge: EdgeData) => ({
        data: edge.data
      }))
    ];

    this.cy = cytoscape({
      container: document.getElementById('cy')!,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#032463',  // Blue color for nodes
            'label': 'data(label)',
            'text-valign': 'center',
            'color': '#fff',
            'text-outline-width': 2,
            'text-outline-color': '#032463',  // Matching outline color
            'font-size': 14,
            'width': 50,
            'height': 50,
            'shape': 'ellipse',
            'border-width': 2,
            'border-color': '#032463'  // Darker blue for border
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 3,
            'line-color': '##333',  // Dark color for edges
            'target-arrow-color': '##333',  // Dark color for arrow
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': '',  // Hide label by default
            'text-wrap': 'wrap',
            'text-max-width': '100px',  // Maximum width for text before wrapping
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': 12,
            'color': '#032463',  // Blue color for the edge label
            'text-background-opacity': 1,
            'text-background-color': '#ffffff',  // Background color for edge label
            'text-background-shape': 'roundrectangle',  // Shape of the background
            'text-border-color': '#032463',  // Border color for the text background
            'text-border-width': 1,
            'text-border-opacity': 1
          }
        },
        {
          selector: 'edge.hover',
          style: {
            'label': 'data(shortenLabel)',  // Display the shortened label on hover
            'text-background-color': '#ffffff',  // Background color for edge label
            'text-background-opacity': 1,
            'z-index': 1000  // High value to ensure the label is on top
          }
        },
        {
          selector: 'node.selected',
          style: {
            'background-color': '#0074D9'  // Highlight color for selected nodes
          }
        },
        {
          selector: 'edge.selected',
          style: {
            'line-color': '#0074D9',  // Highlight color for selected edges
            'target-arrow-color': '#0074D9',  // Highlight color for arrow,
            'text-border-color': '#005bb5',
            'color': '#034baa'
          }
        }
      ],
      layout: {
        name: 'cose',
        animate: true,
        animationDuration: 1000,
        fit: true,  // Automatically fit the graph to the viewport
        padding: 10,
        randomize: false,
        nodeRepulsion: () => 40000000, // Adjusted to match the expected type
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95
      },
      zoom: 100.5,  // Adjust the initial zoom level (1.5x zoom)
      pan: { x: 0, y: 0 },  // Center the graph
    });

    this.cy.on('mouseover', 'edge', (event) => {
      const edge = event.target as cytoscape.EdgeSingular;
      const fullLabel = edge.data('label');
      const shortLabel = this.truncateLabel(fullLabel, 5); // Adjust the number of words as needed

      edge.data('shortenLabel', shortLabel);
      edge.addClass('hover');
    });

    this.cy.on('mouseout', 'edge', (event) => {
      const edge = event.target as cytoscape.EdgeSingular;
      edge.removeClass('hover');
    });

    this.cy.on('click', 'edge', (event) => {
      const edge = event.target as cytoscape.EdgeSingular;
      edge.style('label', edge.data('label'));  // Show the full label on click

      // Hide all other labels
      this.cy.edges().not(edge).style('label', '');

      // Remove highlight from previously selected nodes and edges
      this.cy.nodes().removeClass('selected');
      this.cy.edges().removeClass('selected');

      // Highlight the source and target nodes of the selected edge
      const sourceNode = this.cy.getElementById(edge.data('source'));
      const targetNode = this.cy.getElementById(edge.data('target'));

      sourceNode.addClass('selected');
      targetNode.addClass('selected');
      edge.addClass('selected');
    });

    this.cy.on('tap', (event) => {
      if (event.target === this.cy) {
        this.cy.edges().style('label', '');  // Hide labels when clicking on the background
        this.cy.nodes().removeClass('selected');
        this.cy.edges().removeClass('selected');
      }
    });
  }

  truncateLabel(label: string, maxWords: number): string {
    const words = label.split(' ');
    return words.length > maxWords ? words.slice(0, maxWords).join(' ') + '...' : label;
  }
}
