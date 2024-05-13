# data_loader_interface.py

class DataLoaderInterface:
    def load_data(self, data_path):
        raise NotImplementedError("This method should be overridden by subclasses.")
