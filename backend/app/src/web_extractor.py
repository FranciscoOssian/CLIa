import requests
import html2text
import re
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class WebExtractor:
    def __init__(self):
        self.default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

    def get_html(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": self.default_user_agent}, timeout=10)
            return response.text
        except requests.RequestException:
            logger.error("Erro ao fazer request da URL %s", url)
            return "error on request"

    def extract(self, urls):
        logger.debug("Tentando extrair Markdown das URL's: %s", urls)
        markdowns = []
        for url in urls:
            markdowns.append(self.html_to_markdown(
                self.clean_html(
                    self.get_html(
                        url
                    )
                )
            ))
        return f"""\n========\n""".join(markdowns)

    def clean_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        body = soup.find('body')
        if body:
            for tag in body.find_all(True):
                if tag.name != 'code':
                    tag.attrs = {}
            for tag in body(['header', 'footer', 'nav', 'aside', 'script', 'style']):
                tag.decompose()
            return str(body)
        return ''

    def html_to_markdown(self, html):
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        return h.handle(html)

    def manipulate_markdown(self, markdown_text):
        return re.sub(r'\n\s*\n', '\n\n', markdown_text)
