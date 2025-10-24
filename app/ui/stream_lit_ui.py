# app.py
from neo4j import GraphDatabase
import networkx as nx
from pyvis.network import Network
import streamlit as st
import tempfile

# --- 配置 Neo4j 连接（替换成你的配置） ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "123"

# --- 读取图数据（简单示例） ---
def fetch_graph(limit_nodes=100):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    query = f"""
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT {limit_nodes}
    """
    G = nx.DiGraph()
    with driver.session() as session:
        for record in session.run(query):
            n = record["n"]
            m = record["m"]
            r = record["r"]
            nid = n.id
            mid = m.id
            # use a label or property as title
            nlabel = list(n.labels)[0] if n.labels else "Node"
            mlabel = list(m.labels)[0] if m.labels else "Node"
            G.add_node(nid, title=str(dict(n.items())), label=nlabel)
            G.add_node(mid, title=str(dict(m.items())), label=mlabel)
            G.add_edge(nid, mid, label=r.type)
    driver.close()
    return G

# --- 将 networkx 转成 pyvis html ---
def nx_to_pyvis_html(G, height="600px", width="100%"):
    net = Network(height=height, width=width, notebook=False, directed=True)
    for n, data in G.nodes(data=True):
        net.add_node(n, label=data.get("label", str(n)), title=data.get("title"))
    for u, v, data in G.edges(data=True):
        net.add_edge(u, v, title=data.get("label"))
    net.toggle_physics(True)
    # write to temp file and return html string
    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
    net.show(tmp.name)
    with open(tmp.name, "r", encoding="utf-8") as f:
        html = f.read()
    return html

# --- Streamlit UI ---
st.title("Neo4j Graph Viewer — Streamlit + pyvis")

limit = st.slider("Max relationships to fetch (sampling)", 10, 200, 50)
if st.button("加载图（从 Neo4j）"):
    with st.spinner("从 Neo4j 拉取并渲染..."):
        G = fetch_graph(limit_nodes=limit)
        if len(G) == 0:
            st.warning("没有数据（检查你的 Neo4j 配置与 Cypher 查询）")
        else:
            html = nx_to_pyvis_html(G)
            # 嵌入 HTML
            st.components.v1.html(html, height=700, scrolling=True)

st.markdown("提示：生产环境建议使用 Neovis.js 或 React + Cytoscape 来获得更细粒度的交互控制与性能优化。")
