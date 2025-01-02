import requests
from rdflib import Graph, URIRef, Literal, Namespace
import networkx as nx
import matplotlib.pyplot as plt
import requests
import json


def get_conceptnet_relationships_as_rdf(term, lang="en"):
    base_url = "http://api.conceptnet.io/"
    term_url = f"{base_url}c/{lang}/{term}"
    response = requests.get(term_url).json()
    edges = response.get('edges', [])
    g = Graph()
    CN = Namespace(base_url)
    g.bind("cn", CN)
    for edge in edges:
        start_node = URIRef(edge['start']['@id'])
        end_node = URIRef(edge['end']['@id'])
        predicate = URIRef(edge['rel']['@id'])
        g.add((start_node, predicate, end_node))
    return g

def visualize_rdf_graph(rdf_graph):
    # Convert RDF graph to a NetworkX graph
    nx_graph = nx.DiGraph()
    
    for s, p, o in rdf_graph:
        nx_graph.add_edge(str(s), str(o), label=str(p))
    
    # Draw the graph
    pos = nx.spring_layout(nx_graph)  # Spring layout for better spacing
    plt.figure(figsize=(12, 8))
    
    # Draw nodes and edges
    nx.draw(nx_graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_color="red")
    
    plt.title("RDF Graph Visualization")
    plt.show()


def fetch_raw_conceptnet_data(term, lang="en"):
    base_url = "http://api.conceptnet.io/"
    term_url = f"{base_url}c/{lang}/{term}"
    response = requests.get(term_url)
    return response.json()  # Return the raw JSON response

def extract_relationships(raw_data):
    relationships = []
    
    # Extract relationships from the edges in the raw data
    if "edges" in raw_data:
        for edge in raw_data["edges"]:
            start_node = edge['start']['label']  # Start concept label
            relation = edge['rel']['label']  # Relation type
            end_node = edge['end']['label']  # End concept label
            relationships.append(f"{start_node} -> {relation} -> {end_node}")
    
    return relationships