# utils/helpers.py
import os
import sys
from datetime import datetime


def clear_screen():
    """Xóa màn hình console"""
    if os.name == 'nt':        # Windows
        os.system('cls')
    else:                      # Linux / Mac
        os.system('clear')


def print_header(title: str):
    """In tiêu đề đẹp"""
    print("=" * 70)
    print(f"{' ' * 20}{title:^30}")
    print("=" * 70)


def print_success(message: str):
    print(f"✅ [SUCCESS] {message}")


def print_error(message: str):
    print(f"❌ [ERROR] {message}")


def print_warning(message: str):
    print(f"⚠️  [WARNING] {message}")


def format_date(date_str):
    """Format datetime cho dễ đọc"""
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return str(date_str)


def truncate_text(text: str, max_length: int = 80):
    """Cắt ngắn văn bản"""
    if not text:
        return ""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def is_valid_url(url: str) -> bool:
    """Kiểm tra URL cơ bản"""
    if not url:
        return False
    return url.startswith(('http://', 'https://'))


def get_user_choice(options: list, prompt: str = "Chọn: ") -> str:
    """Hàm hỗ trợ lấy lựa chọn từ người dùng"""
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input(f"\n{prompt}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return choice
        print("Lựa chọn không hợp lệ, vui lòng thử lại!")