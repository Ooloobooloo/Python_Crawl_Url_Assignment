from database.sql_handler import SqlHandler
from models.source import Source

class SourceController:
    def __init__(self):
        self.db = SqlHandler()

    def get_all(self):
        query = """
            SELECT s.*, c.name as category_name
            FROM sources s
            LEFT JOIN categories c ON s.category_id = c.id
            ORDER BY s.id
        """
        return self.db.execute(query, fetchall=True)

    def get_by_id(self, source_id):
        query = "SELECT * FROM sources WHERE id = %s"
        return self.db.execute(query, (source_id,), fetchone=True)

    def add(self, source_name, url, category_id):
        query = "INSERT INTO sources (source_name, url, category_id) VALUES (%s, %s, %s)"
        return self.db.execute(query, (source_name, url, category_id), commit=True)

    def update(self, source_id, source_name, url, category_id):
        query = "UPDATE sources SET source_name = %s, url = %s, category_id = %s WHERE id = %s"
        return self.db.execute(query, (source_name, url, category_id, source_id), commit=True)

    def delete(self, source_id):
        query = "DELETE FROM sources WHERE id = %s"
        return self.db.execute(query, (source_id,), commit=True)

    def get_categories(self):
        return self.db.execute("SELECT * FROM categories ORDER BY name", fetchall=True)
