import os
import shutil
from datetime import datetime
import json
import argparse
import logging

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    file_handler = logging.FileHandler('backup.log')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False


def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        if "sources" not in config or "destination" not in config:
            logging.error("Config file must contain 'sources' (list) and 'destination' (string).")
            return None
        if not isinstance(config["sources"], list):
            logging.error("'sources' in config must be a list.")
            return None
        if not isinstance(config["destination"], str):
            logging.error("'destination' in config must be a string.")
            return None
        config.setdefault("archive_format", "zip")
        logging.info(f"Configuration loaded successfully from {config_path}")
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found at '{config_path}'")
        return None
    except json.JSONDecodeError:
        logging.error(f"Could not decode JSON from '{config_path}'. Check for syntax errors.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred loading config: {e}", exc_info=True)
        return None

def create_backup_archive(source_path, destination_base_path, archive_format="zip"):
    logging.info(f"Attempting to back up: {source_path} (format: {archive_format})")
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source_name = os.path.basename(os.path.normpath(source_path))
        
        archive_filename_base = f"{source_name}_{timestamp}"
        output_archive_basepath = os.path.join(destination_base_path, archive_filename_base)

        os.makedirs(destination_base_path, exist_ok=True)

        archive_path = shutil.make_archive(
            base_name=output_archive_basepath,
            format=archive_format,
            root_dir=source_path
        )
        logging.info(f"Successfully created backup: {archive_path}")
        return archive_path
    except FileNotFoundError:
        logging.error(f"Source directory not found at '{source_path}'")
        return None
    except Exception as e:
        logging.error(f"Error creating backup for '{source_path}': {e}", exc_info=True)
        return None

def main(config_data):
    logging.info("Backup Utility Started")
    logging.info("----------------------")
    
    source_directories = config_data["sources"]
    destination_directory = config_data["destination"]
    archive_format = config_data.get("archive_format", "zip")

    logging.info("Effective Configuration:")
    logging.info(f"  Sources to back up: {source_directories}")
    logging.info(f"  Destination for backups: {destination_directory}")
    logging.info(f"  Archive format: {archive_format}")
    logging.info("----------------------")

    if not source_directories:
        logging.warning("No source directories configured. Exiting.")
        return
    
    if not os.path.exists(destination_directory):
        try:
            os.makedirs(destination_directory)
            logging.info(f"Created destination directory: {destination_directory}")
        except Exception as e:
            logging.error(f"Could not create destination directory '{destination_directory}': {e}", exc_info=True)
            return

    successful_backups = 0
    failed_backups = 0

    for source_path in source_directories:
        source_path = os.path.normpath(source_path)
        if not os.path.exists(source_path):
            logging.warning(f"Source path '{source_path}' does not exist. Skipping.")
            failed_backups += 1
            continue

        logging.info(f"Processing source: {source_path}")
        archive_created_path = create_backup_archive(source_path, destination_directory, archive_format)
        if archive_created_path:
            successful_backups += 1
        else:
            failed_backups += 1
    
    logging.info("--- Backup Summary ---")
    logging.info(f"Total sources configured: {len(source_directories)}")
    logging.info(f"Successful backups: {successful_backups}")
    logging.info(f"Failed backups: {failed_backups}")
    logging.info("----------------------")
    logging.info("Backup Utility Finished")

if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(description="Simple Backup Utility with Logging.")
    parser.add_argument("-c", "--config",
                        default="backup_config.json",
                        help="Path to the JSON configuration file (default: backup_config.json)")
    
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if config:
        main(config)
    else:
        logging.error("Exiting due to configuration errors.")