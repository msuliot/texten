# texten - TEXT Extraction Node
import os
import hashlib
import json
import re
import fnmatch
import logging
from config_manager import ConfigManager
from msuliot.data_loader_manager import DataLoaderManager # https://github.com/msuliot/package.data.loaders.git
from msuliot.base_64 import Base64 # https://github.com/msuliot/package.utils.git

log_filename = 'texten.log' 
logging.basicConfig(filename=log_filename,
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

pii_files_count = 0 
total_pii_count = 0 
converted_files_count = 0 

config_manager = ConfigManager()
config = config_manager.config
pii_ok = config_manager.pii_ok
exclusions = config_manager.exclusions


def print_and_log(message):
    logging.info(message)
    print(message)


def is_excluded(path, exclusions):
    for pattern in exclusions:
        if fnmatch.fnmatch(path, pattern):
            logging.info(f"Skipping excluded file or directory: {path}")
            return True
        
    return False


def is_startswith_excluded(file):
    if file.startswith('~$') or file.startswith('.'):
        logging.info(f"Skipping excluded file or directory: {file}")
        return True
    
    return False


def find_pii(text, patterns):
    pii_found = {}

    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            pii_found[pii_type] = list(set(matches))

    return pii_found


def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()

    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return None
    
    try:
        with open(filepath, "rb") as f:

            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

    except IOError as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return None
    
    return sha256_hash.hexdigest()


def load_pii_ok(pii_ok_file_path):
    try:
        with open(pii_ok_file_path, 'r') as file:
            return json.load(file)
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading pii_ok from {pii_ok_file_path}: {e}")
        return []


def load_hashes(hash_file_path):
    try:
        with open(hash_file_path, "r") as file:
            return json.load(file)
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"Error loading hashes from {hash_file_path}: {e}")
        return {}


def save_hashes(hash_file_path, hashes):
    try:
        with open(hash_file_path, "w") as file:
            json.dump(hashes, file, indent=4)

    except IOError as e:
        logging.error(f"Error saving hashes to {hash_file_path}: {e}")
        return False


def save_pii_text(filename, text, output_directory, source_file_path, flagged_content):
    global pii_files_count 

    try:
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, filename)
        flagged_text = json.dumps(flagged_content, indent=4)
        text_with_paths_and_flags = f"Source File Path: {source_file_path}\nOutput Path and Filename: {output_path}\nFlagged Content:\n{flagged_text}\n\n{text}"
        
        with open(output_path, 'w') as file:
            file.write(text_with_paths_and_flags)
        
        pii_files_count += 1
        logging.info(f"File saved successfully with PII content: {output_path}")

    except Exception as e:
        logging.error(f"Error saving text to {output_path}: {e}")
        return False

def save_text(filename, text, output_directory, source_file_path):
    global converted_files_count

    try:
        
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, filename)
        
        with open(output_path, 'w') as file:
            file.write(text)

        converted_files_count += 1
        logging.info(f"File saved successfully text file: {output_path}")

    except Exception as e:
        logging.error(f"Error saving text to {output_path}: {e}")

def convert_and_save(file_path, config):
    global total_pii_count
    
    dlm = DataLoaderManager()

    text_output_directory = config.get('text_output_directory', '.')
    pii_output_directory = config.get('pii_output_directory', '.')
    hash_file_path = config.get('hash_file_path', 'file_hashes.json')
    hashes = load_hashes(hash_file_path)
    file_path_base64 = Base64.encode(file_path)
    patterns = config.get('patterns', {})
    print(".", end="", flush=True)
    file_hash = calculate_file_hash(file_path)
    
    if file_hash is None or hashes.get(file_path) == file_hash:
        return
    
    text_filename = f"{file_path_base64}.txt"
    text = ""
    
    try:
        text = dlm.load_data(file_path, file_path.split('.')[-1])

        if text:
            is_pii_ok = False

            if file_path in pii_ok:
                is_pii_ok = True
            
            pii_found = find_pii(text, patterns)

            if pii_found and not is_pii_ok:
                logging.info(f"PII detected in {file_path}") # : {pii_found}")  # Commented out to avoid logging pii content
                total_pii_count += sum(len(matches) for matches in pii_found.values())
                save_pii_text(text_filename, text, pii_output_directory, file_path, pii_found)
            else:
                save_text(text_filename, text, text_output_directory, file_path)
                hashes[file_path] = file_hash
                save_hashes(hash_file_path, hashes)

        else:
            logging.error(f"Could not convert file {file_path}")
            return False

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return False


def main():
    global pii_files_count, total_pii_count, converted_files_count

    for input_directory in config.get('input_directories', []):
        for root, dirs, files in os.walk(input_directory):
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclusions)]  # exclude directories
            for file in files:

                file_path = os.path.join(root, file)

                if is_startswith_excluded(file): # exclude files starting with ~$ or .
                    continue

                if is_excluded(file_path, exclusions): # exclude files
                    continue
                
                dlm = DataLoaderManager()
                if file_path.split('.')[-1].lower() in dlm.get_supported_data_loaders():
                    convert_and_save(file_path, config)
    
    print_and_log(f"Total converted files: {converted_files_count}")
    print_and_log(f"Total PII files: {pii_files_count}")
    print_and_log(f"Total PII instances detected: {total_pii_count}")


if __name__ == "__main__":
    print("\nProcess started:", end=" ")
    main()
    print("\nTextify process complete. Check logs for details.") 