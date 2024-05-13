import pandas as pd
import openpyxl
import logging
from data_loaders.data_loader_interface import DataLoaderInterface

class XlsxLoader(DataLoaderInterface):
    
    
    def load_data(self, data_path):
        text = self.convert_xlsx_to_txt(data_path)
        return text


    def convert_xlsx_to_txt(self, filepath):
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
        except Exception as e:
            logging.error(f"Error reading XLSX file {filepath}: {e}")
            return ""
        return df.to_csv(index=False)
    

# def convert_xls_to_txt(filepath):
#     try:
#         book = xlrd.open_workbook(filepath)
#     except Exception as e:
#         logging.error(f"Error reading XLS file {filepath}: {e}")
#         return ""
    
#     first_sheet = book.sheet_by_index(0)
#     data = []
#     for row in range(first_sheet.nrows):
#         data.append(first_sheet.row_values(row))
#     return "\n".join([",".join(map(str, row)) for row in data])