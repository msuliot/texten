import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from data_loaders.data_loader_interface import DataLoaderInterface
from data_loaders.data_loader_manager import DataLoaderManager
from msuliot.base_64 import Base64

class WebsiteCrawler(DataLoaderInterface):

    def load_data(self, root_url):
        self.visited_urls = set()
        self.output_dir = '/Users/msuliot/Desktop/text_output'

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.crawl(root_url)

    def crawl(self, url):
        if url in self.visited_urls:
            return
        
        print(f"Crawling: {url}")
        self.visited_urls.add(url)

        html_content = self.fetch_html_from_url(url)

        if html_content:
            self.save_content(url, html_content)
            for link in self.extract_links(url, html_content):
                self.crawl(link)

    def fetch_html_from_url(self, url):
        dlm = DataLoaderManager()
        try:
            if url.lower().endswith('.pdf'):
                text = dlm.load_data(url, 'pdf')
            else:
                text = dlm.load_data(url, 'html')

            return text
            
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def extract_links(self, base_url, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            if self.is_same_domain(base_url, full_url) and full_url not in self.visited_urls:
                yield full_url


    def is_same_domain(self, base_url, url):
        return urlparse(base_url).netloc == urlparse(url).netloc


    def save_content(self, url, html_content):
        url = url.split('?')[0]
        soup = BeautifulSoup(html_content, 'html.parser')
        text_elements = soup.select('p, h1, h2, h3, h4, h5, h6')
        text_content = ' '.join(element.get_text(' ', strip=True) for element in text_elements)
        file_path_base64 = Base64.encode(url.split('?')[0])
        text_filename = f"{file_path_base64}.txt"
        filepath = os.path.join(self.output_dir, text_filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text_content)

        print(f"Saved text content to: {filepath}")