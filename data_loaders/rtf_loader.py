import logging

from data_loaders.data_loader_interface import DataLoaderInterface

class RtfLoader(DataLoaderInterface):
    

    def load_data(self, data_path):
        text = self.convert_rtf_to_txt(data_path)
        return text


    def convert_rtf_to_txt(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except IOError as e:
            logging.error(f"Error reading RTF file {filepath}: {e}")
            return ""