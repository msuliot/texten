import json
import logging

class ConfigManager:
    def __init__(self):
        self.config = self.load_config('config.json')
        self.pii_ok = self.load_pii_ok('pii_ok_list.json')
        self.exclusions = self.load_exclusions('exclusion_list.json')

    def load_config(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading config from {filepath}: {e}")
            return {}

    def load_pii_ok(self, filepath):
        return self.load_config(filepath)

    def load_exclusions(self, filepath):
        return self.load_config(filepath)
