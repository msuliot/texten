import fitz  # Use PyMuPDF for PDF handling
import logging
import requests
from data_loaders.data_loader_interface import DataLoaderInterface

class PdfLoader(DataLoaderInterface):
    
    def load_data(self, data_path):
        text = self.convert_pdf_to_txt(data_path)
        return text

    def is_url(self, path):
        """Check if the given path is a URL."""
        return path.startswith('http://') or path.startswith('https://')

    def convert_pdf_to_txt(self, path):
        text = ""
        try:
            if self.is_url(path):
                response = requests.get(path)
                response.raise_for_status()
                doc = fitz.open(stream=response.content, filetype="pdf")
            else:
                doc = fitz.open(path)
            
            if doc.is_encrypted:
                logging.error(f"PDF file is password-protected and cannot be opened: {path}")
                return ""
            
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            logging.error(f"Error processing PDF file {path}: {e}")
            return ""
        
        return text
