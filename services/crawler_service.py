import requests
from bs4 import BeautifulSoup
from config import HEADERS
from crawlers.parser import get_parser
from database.sql_handler import SqlHandler

class CrawlerService:
    def __init__(self):
        self.db = SqlHandler()

    def crawl_list_links(self):
        sources = self.db.execute("SELECT id, url, category_id FROM sources", fetchall=True) or []
        if not sources:
            print("⚠️ Không tìm thấy nguồn tin trong database.")
            return

        for source in sources:
            source_id = source['id']
            url = source['url']
            category_id = source.get('category_id')
            try:
                response = requests.get(url, headers=HEADERS, timeout=15)
                response.raise_for_status()
            except Exception as e:
                print(f"❌ Lỗi tải nguồn {url}: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            parser = get_parser(url)
            articles = parser.extract_list(soup)
            saved = 0

            for article in articles:
                if not article.get('url') or not article.get('title'):
                    continue

                existing = self.db.execute(
                    "SELECT id FROM articles WHERE url = %s", (article['url'],), fetchone=True
                )
                if existing:
                    continue

                self.db.execute(
                    "INSERT INTO articles (title, url, summary, content, status, source_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (article['title'], article['url'], "", "", 0, source_id, category_id),
                    commit=True
                )
                saved += 1

            print(f"✅ Source {source_id}: thêm {saved} link mới từ {url}")

        print("✅ Hoàn tất crawl danh sách link.")

    def crawl_details(self):
        articles = self.db.execute(
            "SELECT id, url FROM articles WHERE status = 0", fetchall=True
        ) or []
        if not articles:
            print("⚠️ Không có bài viết nào cần crawl nội dung.")
            return

        for article in articles:
            article_id = article['id']
            url = article['url']
            try:
                response = requests.get(url, headers=HEADERS, timeout=15)
                response.raise_for_status()
            except Exception as e:
                print(f"❌ Lỗi tải bài viết {url}: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = [p.get_text(strip=True) for p in soup.select("p") if p.get_text(strip=True)]
            content = "\n\n".join(paragraphs).strip()
            summary = content[:200] if content else ""

            self.db.execute(
                "UPDATE articles SET summary = %s, content = %s, status = %s WHERE id = %s",
                (summary, content, 1, article_id),
                commit=True
            )

            print(f"✅ Cập nhật nội dung bài viết #{article_id}")

        print("✅ Hoàn tất crawl nội dung.")
