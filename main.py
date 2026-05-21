# main.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from controllers.source_controller import SourceController
from controllers.article_controller import ArticleController
from controllers.category_controller import CategoryController
from services.crawler_service import CrawlerService
from services.scheduler_service import SchedulerService
import sys

console = Console()

def clear_screen():
    console.clear()

def main_menu():
    source_ctrl = SourceController()
    article_ctrl = ArticleController()
    category_ctrl = CategoryController()
    crawler = CrawlerService()

    while True:
        clear_screen()
        console.print(Panel.fit("[bold cyan]NEWS AGGREGATOR CLI - PROFESSIONAL[/bold cyan]", border_style="blue"))

        console.print("\n[bold]1.[/bold] Quản lý Nguồn tin")
        console.print("[bold]2.[/bold] Xem Tin tức (Phân trang)")
        console.print("[bold]3.[/bold] Crawl Danh sách Link ngay")
        console.print("[bold]4.[/bold] Crawl Nội dung ngay")
        console.print("[bold]5.[/bold] Bật Scheduler (Cronjob)")
        console.print("[bold red]0.[/bold red] Thoát")

        choice = console.input("\n[bold yellow]Chọn chức năng → [/bold yellow]")

        if choice == '1':
            manage_sources(source_ctrl, category_ctrl)
        elif choice == '2':
            view_articles(article_ctrl)
        elif choice == '3':
            console.print("[green]Đang crawl danh sách link...[/green]")
            crawler.crawl_list_links()
            console.input("\nNhấn Enter để tiếp tục...")
        elif choice == '4':
            console.print("[green]Đang crawl nội dung...[/green]")
            crawler.crawl_details()
            console.input("\nNhấn Enter để tiếp tục...")
        elif choice == '5':
            SchedulerService.start()
        elif choice == '0':
            console.print("[red]Tạm biệt![/red]")
            sys.exit(0)

def manage_sources(ctrl, category_ctrl):
    while True:
        console.print("\n[bold]=== QUẢN LÝ NGUỒN TIN ===[/bold]")
        console.print("1. Xem danh sách\n2. Thêm nguồn mới\n3. Chỉnh sửa nguồn\n4. Xóa nguồn\n5. Quản lý danh mục\n0. Quay lại")
        ch = console.input("Chọn: ")
        if ch == '1':
            sources = ctrl.get_all() or []
            table = Table()
            table.add_column("ID")
            table.add_column("Tên nguồn")
            table.add_column("Danh mục")
            table.add_column("URL")
            for s in sources:
                table.add_row(str(s['id']), s['source_name'], s['category_name'] or "-", s['url'][:50])
            console.print(table)
        elif ch == '2':
            categories = ctrl.get_categories() or []
            if not categories:
                console.print("[yellow]Chưa có danh mục nào. Vui lòng thêm danh mục trước.[/yellow]")
                continue

            console.print("[bold]Danh sách danh mục:[/bold]")
            for c in categories:
                console.print(f"- {c['name']}")

            while True:
                category_name = console.input("Nhập tên danh mục: ").strip()
                if not category_name:
                    console.print("[red]Bạn phải nhập tên danh mục.[/red]")
                    continue

                matched = [c for c in categories if c['name'].strip().lower() == category_name.lower()]
                if len(matched) == 1:
                    cat_id = matched[0]['id']
                    break
                if len(matched) > 1:
                    console.print("[red]Có nhiều danh mục cùng tên. Vui lòng nhập tên chính xác hơn.[/red]")
                    continue

                console.print("[red]Không tìm thấy danh mục. Nhập lại tên chính xác.[/red]")

            name = console.input("Tên nguồn: ").strip()
            url = console.input("URL: ").strip()
            if name and url and ctrl.add(name, url, cat_id):
                console.print("[green]Thêm thành công![/green]")
            else:
                console.print("[red]Thêm nguồn không thành công. Vui lòng kiểm tra lại.[/red]")
        elif ch == '3':
            sources = ctrl.get_all() or []
            if not sources:
                console.print("[yellow]Chưa có nguồn nào để sửa.[/yellow]")
                continue
            for s in sources:
                console.print(f"{s['id']}. {s['source_name']} ({s['category_name'] or 'Chưa có'})")
            source_id = console.input("Nhập ID nguồn muốn sửa: ").strip()
            if not source_id.isdigit():
                console.print("[red]ID không hợp lệ.[/red]")
                continue
            source = ctrl.get_by_id(int(source_id))
            if not source:
                console.print("[red]Không tìm thấy nguồn này.[/red]")
                continue

            categories = ctrl.get_categories() or []
            console.print("[bold]Danh sách danh mục:[/bold]")
            for c in categories:
                console.print(f"- {c['name']}")

            category_name = console.input(f"Tên danh mục mới ({source.get('category_id') or 'Không đổi'}): ").strip()
            if category_name:
                matched = [c for c in categories if c['name'].strip().lower() == category_name.lower()]
                if not matched:
                    console.print("[red]Danh mục không tồn tại.[/red]")
                    continue
                category_id = matched[0]['id']
            else:
                category_id = source.get('category_id')

            name = console.input(f"Tên nguồn mới ({source.get('source_name')}): ").strip() or source.get('source_name')
            url = console.input(f"URL mới ({source.get('url')}): ").strip() or source.get('url')
            if ctrl.update(int(source_id), name, url, category_id):
                console.print("[green]Cập nhật nguồn thành công![/green]")
            else:
                console.print("[red]Cập nhật không thành công.[/red]")
        elif ch == '4':
            sources = ctrl.get_all() or []
            if not sources:
                console.print("[yellow]Chưa có nguồn nào để xóa.[/yellow]")
                continue
            for s in sources:
                console.print(f"{s['id']}. {s['source_name']} ({s['category_name'] or 'Chưa có'})")
            source_id = console.input("Nhập ID nguồn muốn xóa: ").strip()
            if not source_id.isdigit():
                console.print("[red]ID không hợp lệ.[/red]")
                continue
            if ctrl.delete(int(source_id)):
                console.print("[green]Xóa nguồn thành công![/green]")
            else:
                console.print("[red]Xóa nguồn không thành công.[/red]")
        elif ch == '5':
            manage_categories(category_ctrl)
        elif ch == '0':
            break

def view_articles(ctrl):
    page = 0
    while True:
        articles = ctrl.get_paginated(page) or []
        table = Table(title=f"Trang {page + 1}")
        table.add_column("ID")
        table.add_column("Tiêu đề")
        table.add_column("Nguồn")
        table.add_column("Danh mục")
        table.add_column("Trạng thái")
        for a in articles:
            status = "[green]Đã crawl[/green]" if a['status'] == 1 else "[yellow]Chưa[/yellow]"
            table.add_row(
                str(a['id']),
                (a['title'] or "")[:60],
                a['source_name'] or "-",
                a['category_name'] or "-",
                status,
            )
        console.print(table)

        console.print("\n[N] Next | [P] Previous | [Q] Quay lại")
        key = console.input("→ ").strip().upper()
        if key == 'N':
            page += 1
        elif key == 'P' and page > 0:
            page -= 1
        elif key == 'Q':
            break


def manage_categories(ctrl):
    while True:
        console.print("\n[bold]=== QUẢN LÝ DANH MỤC ===[/bold]")
        console.print("1. Xem danh sách\n2. Thêm danh mục\n3. Sửa danh mục\n4. Xóa danh mục\n0. Quay lại")
        ch = console.input("Chọn: ")
        if ch == '1':
            categories = ctrl.get_all() or []
            table = Table()
            table.add_column("ID")
            table.add_column("Tên danh mục")
            for c in categories:
                table.add_row(str(c['id']), c['name'])
            console.print(table)
        elif ch == '2':
            name = console.input("Tên danh mục mới: ").strip()
            if name and ctrl.add(name):
                console.print("[green]Thêm danh mục thành công![/green]")
            else:
                console.print("[red]Thêm danh mục không thành công.[/red]")
        elif ch == '3':
            categories = ctrl.get_all() or []
            if not categories:
                console.print("[yellow]Chưa có danh mục nào để sửa.[/yellow]")
                continue
            for c in categories:
                console.print(f"{c['id']}. {c['name']}")
            category_id = console.input("Nhập ID danh mục muốn sửa: ").strip()
            if not category_id.isdigit():
                console.print("[red]ID không hợp lệ.[/red]")
                continue
            name = console.input("Tên danh mục mới: ").strip()
            if name and ctrl.update(int(category_id), name):
                console.print("[green]Cập nhật danh mục thành công![/green]")
            else:
                console.print("[red]Cập nhật không thành công.[/red]")
        elif ch == '4':
            categories = ctrl.get_all() or []
            if not categories:
                console.print("[yellow]Chưa có danh mục nào để xóa.[/yellow]")
                continue
            for c in categories:
                console.print(f"{c['id']}. {c['name']}")
            category_id = console.input("Nhập ID danh mục muốn xóa: ").strip()
            if not category_id.isdigit():
                console.print("[red]ID không hợp lệ.[/red]")
                continue
            if ctrl.delete(int(category_id)):
                console.print("[green]Xóa danh mục thành công![/green]")
            else:
                console.print("[red]Xóa danh mục không thành công.[/red]")
        elif ch == '0':
            break

if __name__ == "__main__":
    main_menu()