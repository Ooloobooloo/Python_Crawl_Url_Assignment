import schedule
import time
from services.crawler_service import CrawlerService

class SchedulerService:
    @staticmethod
    def start():
        crawler = CrawlerService()
        print("🚀 Scheduler đang chạy... (Ctrl + C để dừng)")

        schedule.every().day.at("08:00").do(crawler.crawl_list_links)
        schedule.every(30).minutes.do(crawler.crawl_details)

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Scheduler đã dừng lại. Quay về menu chính.")