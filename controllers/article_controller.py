from database.sql_handler import SqlHandler

class ArticleController:
    def __init__(self):
        self.db = SqlHandler()

    def get_paginated(self, page=0, per_page=10):
        offset = page * per_page
        query = """
            SELECT a.id, a.title, a.url, a.summary, a.status, a.created_at,
                   s.source_name, c.name AS category_name
            FROM articles a
            LEFT JOIN sources s ON a.source_id = s.id
            LEFT JOIN categories c ON a.category_id = c.id
            ORDER BY a.created_at DESC
            LIMIT %s OFFSET %s
        """
        return self.db.execute(query, (per_page, offset), fetchall=True)
