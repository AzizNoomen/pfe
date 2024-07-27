from neo4j import GraphDatabase
from app.exceptions.service_exceptions import OopsNoDBError

class DBHelper:
    def __init__(self, db_url: str, user: str, password: str):
        self.db_url = db_url
        self.user = user
        self.password = password
        self.driver = None

    def init_database(self):
        """Initialize the database connection."""
        if not self.driver:
            self.driver = GraphDatabase.driver(
                self.db_url,
                auth=(self.user, self.password)
            )
        return self.driver

    def session(self):
        """Get a new session from the driver."""
        if not self.driver:
            raise OopsNoDBError("Database driver not initialized.")
        return self.driver.session()

    def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()
            self.driver = None
