import networkx as nx
from pathlib import Path

from src.graph_pipeline import build_graph, draw_graph, compute_layout

G = nx.Graph()

while True:
    aaa = input("Default visualization:(Y/N): ")
    if aaa == "Y":
        progress_percents = build_graph(G)
        break
    elif aaa == "N":
        json_path = input("input the json path you want to visualize: ")
        path = Path(json_path)
        progress_percents = build_graph(G, path)
        break
    else:
        continue

pos = compute_layout(G)
draw_graph(G=G, pos=pos, progress_percents=progress_percents)
