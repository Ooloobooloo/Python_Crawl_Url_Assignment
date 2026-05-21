from database.sql_handler import SqlHandler

class CategoryController:
    def __init__(self):
        self.db = SqlHandler()

    def get_all(self):
        return self.db.execute("SELECT * FROM categories ORDER BY name", fetchall=True)

    def add(self, name):
        return self.db.execute("INSERT INTO categories (name) VALUES (%s)", (name,), commit=True)

    def update(self, category_id, name):
        return self.db.execute(
            "UPDATE categories SET name = %s WHERE id = %s",
            (name, category_id),
            commit=True
        )

    def delete(self, category_id):
        return self.db.execute(
            "DELETE FROM categories WHERE id = %s",
            (category_id,),
            commit=True
        )
