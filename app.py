import threading
import configparser
from tkinter import Tk, filedialog, messagebox
from gui.main_window import MainWindow
from gdrive.auth import authenticate
from gdrive.utils import create_folder_structure, get_all_files, download_files, check_existing_files
from gui.utils import update_progress_bar

pause_event = threading.Event()
stop_event = threading.Event()

CONFIG_FILE = "config.ini"

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'SETTINGS' not in config:
        config['SETTINGS'] = {
            'folder_id': '',
            'destination': ''
        }
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def start_download(folder_id, destination, canvas, labels):
    service = authenticate()

    # Create the folder structure
    canvas.itemconfig(labels['status_label'], text="Creating folder structure...")
    create_folder_structure(service, folder_id, destination)

    # Get all files metadata
    canvas.itemconfig(labels['status_label'], text="Fetching file list...")
    all_files = get_all_files(service, folder_id, destination)

    # Check existing files and filter out those that need to be re-downloaded
    canvas.itemconfig(labels['status_label'], text="Checking existing files...")
    update_progress_bar(0, is_verification=True, canvas=canvas)

    files_to_download = check_existing_files(all_files, canvas, labels)

    # Update UI with total file count
    total_files = len(all_files)
    canvas.itemconfig(labels['total_progress_label'], text=f"{total_files}/{len(files_to_download)}")
    update_progress_bar(0, canvas=canvas)

    # Download the files
    canvas.itemconfig(labels['status_label'], text="Downloading files...")
    download_files(service, files_to_download, canvas, labels, pause_event, stop_event)

    # Final message
    canvas.itemconfig(labels['status_label'], text="Download and verification completed")

def browse_destination(entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, 'end')
        entry.insert(0, folder_selected)

def main():
    config = load_config()
    window = Tk()
    app = MainWindow(window, start_download, browse_destination, pause_event, stop_event, config)
    window.resizable(False, False)
    window.mainloop()
    save_config(config)

if __name__ == "__main__":
    main()
