# database/sql_handler.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class SqlHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_connection(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            self.initialize_schema(conn)
            return conn
        except Error as e:
            if hasattr(e, 'errno') and e.errno == 1049:
                if self.create_database():
                    try:
                        conn = mysql.connector.connect(**DB_CONFIG)
                        self.initialize_schema(conn)
                        return conn
                    except Error as second_e:
                        print(f"❌ Database Error after create: {second_e}")
                        return None
            print(f"❌ Database Error: {e}")
            return None

    def create_database(self):
        config = DB_CONFIG.copy()
        config.pop('database', None)
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Database '{DB_CONFIG['database']}' đã được tạo (nếu chưa tồn tại).")
            return True
        except Error as e:
            print(f"❌ Lỗi tạo database: {e}")
            return False

    def column_exists(self, conn, table_name, column_name):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND column_name = %s",
            (DB_CONFIG['database'], table_name, column_name)
        )
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        return exists

    def initialize_schema(self, conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sources (
                id INT AUTO_INCREMENT PRIMARY KEY,
                source_name VARCHAR(255) NOT NULL,
                url TEXT NOT NULL,
                category_id INT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
                    ON DELETE SET NULL ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title TEXT,
                url TEXT NOT NULL UNIQUE,
                summary TEXT,
                content LONGTEXT,
                status TINYINT DEFAULT 0,
                source_id INT,
                category_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES sources(id)
                    ON DELETE SET NULL ON UPDATE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id)
                    ON DELETE SET NULL ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        conn.commit()
        cursor.close()

        if not self.column_exists(conn, 'articles', 'category_id'):
            alter = conn.cursor()
            alter.execute("ALTER TABLE articles ADD COLUMN category_id INT NULL")
            alter.execute(
                "ALTER TABLE articles ADD CONSTRAINT fk_articles_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL ON UPDATE CASCADE"
            )
            conn.commit()
            alter.close()

        self.seed_categories(conn)

    def seed_categories(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        if count == 0:
            default_categories = [
                'Công nghệ',
                'Kinh doanh',
                'Thể thao',
                'Giải trí',
                'Thời sự'
            ]
            for name in default_categories:
                cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
            conn.commit()
            print("✅ Đã seed dữ liệu danh mục mặc định.")
        cursor.close()

    def execute(self, query, params=None, fetchone=False, fetchall=False, commit=False):
        conn = self.get_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return cursor.rowcount
        except Error as e:
            print(f"❌ Query Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
