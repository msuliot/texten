import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from data_loaders.data_loader_interface import DataLoaderInterface
import logging

class HtmlLoader(DataLoaderInterface):

    def load_data(self, data_path):
        text = self.convert_html_to_txt(data_path)
        return text

    def convert_html_to_txt(self, path):
        if self.is_url(path):
            html_content = self.fetch_html_from_url(path)
        else:
            html_content = self.read_html_from_file(path)
        
        return html_content

    def is_url(self, path):
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def fetch_html_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return None


    def read_html_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
