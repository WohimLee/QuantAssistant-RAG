
import pandas as pd
from neo4j import GraphDatabase

def connect():
    # 替换为你的实际连接地址和密码
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "123"

    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver


def get_db_overview(tx):
    # 节点总数
    node_count = tx.run("MATCH (n) RETURN count(n) AS nodes").single()["nodes"]

    # 关系总数
    rel_count = tx.run("MATCH ()-[r]->() RETURN count(r) AS relationships").single()["relationships"]

    # 按标签统计节点数量
    labels = tx.run("""
        MATCH (n)
        RETURN labels(n) AS labels, count(*) AS count
        ORDER BY count DESC
    """).data()

    # 按关系类型统计数量
    rels = tx.run("""
        MATCH ()-[r]->()
        RETURN type(r) AS relationship_type, count(*) AS count
        ORDER BY count DESC
    """).data()

    return {
        "nodes": node_count,
        "relationships": rel_count,
        "labels": labels,
        "relationship_types": rels
    }


def create_nodes_tx(tx, labels_cypher, items):

    query = f"""
    UNWIND $items AS properbilities
    CREATE (n{labels_cypher})
    SET n = properbilities
    """
    tx.run(query, items=items)
    return


if __name__ == "__main__":

    stock_list = "app/data/tushare_data/stock_list_2025-10-24_17_51.csv"
    stock_list_df = pd.read_csv(stock_list)


    pass
