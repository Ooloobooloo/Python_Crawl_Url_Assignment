from bs4 import BeautifulSoup

def get_parser(url):
    if 'vnexpress.net' in url:
        return VnExpressParser()
    elif 'tuoitre.vn' in url:
        return TuoiTreParser()
    else:
        return BaseParser()

class BaseParser:
    def extract_list(self, soup):
        articles = []
        for a in soup.select('a[href]')[:15]:
            title = a.get_text(strip=True)
            href = a.get('href')
            if title and href and len(title) > 10:
                articles.append({'title': title, 'url': href})
        return articles

class VnExpressParser(BaseParser):
    def extract_list(self, soup):
        articles = []
        for item in soup.select('article.item-news'):
            a = item.select_one('h3.title-news a')
            if a:
                title = a.get_text(strip=True)
                url = a.get('href')
                if url and title:
                    if not url.startswith('http'):
                        url = 'https://vnexpress.net' + url
                    articles.append({'title': title, 'url': url})
        return articles

class TuoiTreParser(BaseParser):
    def extract_list(self, soup):
        articles = []
        for h in soup.select('h3 a'):
            title = h.get_text(strip=True)
            url = h.get('href')
            if url and title:
                if not url.startswith('http'):
                    url = 'https://tuoitre.vn' + url
                articles.append({'title': title, 'url': url})
        return articles