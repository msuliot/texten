import pandas as pd
import logging
from data_loaders.data_loader_interface import DataLoaderInterface

class CsvLoader(DataLoaderInterface):
    
    def load_data(self, data_path):
        text = self.convert_csv_to_txt(data_path)
        return text

    def convert_csv_to_txt(self, filepath):
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            logging.error(f"Error reading CSV file {filepath}: {e}")
            return ""
        return df.to_csv(index=False)