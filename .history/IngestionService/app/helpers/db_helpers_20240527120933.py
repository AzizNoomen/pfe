from neo4j import GraphDatabase

class Neo4jHelper:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def run_query(self, query, **kwargs):
        with self._driver.session() as session:
            result = session.run(query, **kwargs)
            return result

    def create_node(self, label, properties):
        query = f"CREATE (n:{label} {{"
        query += ", ".join([f"{key}: '{value}'" for key, value in properties.items()])
        query += "})"
        return self.run_query(query)

    def get_node_by_id(self, node_id):
        query = f"MATCH (n) WHERE ID(n) = {node_id} RETURN n"
        return self.run_query(query)

    # Add more methods as needed for your application
