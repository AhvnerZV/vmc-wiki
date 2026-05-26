"""
graph.py
Builds the force-directed graph from wiki page relationships.
Players = large nodes, Concepts = smaller nodes, edges = connections.
"""

from .models import WikiPage, WikiGraph, GraphNode, GraphLink


def build_graph(players: list[WikiPage], concepts: list[WikiPage]) -> WikiGraph:
    nodes: list[GraphNode] = []
    links: list[GraphLink] = []
    all_ids = {p.id for p in players} | {c.id for c in concepts}

    for p in players:
        nodes.append(GraphNode(id=p.id, label=p.title, type="player", size=22))

    for c in concepts:
        nodes.append(GraphNode(id=c.id, label=c.title, type="concept", size=12))

    seen_links: set[tuple[str, str]] = set()

    def add_link(source: str, target: str, strength: float = 1.0):
        key = tuple(sorted([source, target]))
        if key not in seen_links and source in all_ids and target in all_ids:
            seen_links.add(key)
            links.append(GraphLink(source=source, target=target, strength=strength))

    for page in players + concepts:
        for related_ref in page.related:
            slug = related_ref.lower().replace(" ", "-")
            slug = "".join(c if c.isalnum() or c == "-" else "" for c in slug)
            for candidate_id in all_ids:
                if slug in candidate_id or candidate_id in slug:
                    add_link(page.id, candidate_id)
                    break

    return WikiGraph(nodes=nodes, links=links)
