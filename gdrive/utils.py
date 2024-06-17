import os
from googleapiclient.http import MediaIoBaseDownload
import io
import time
from utils.file_utils import calculate_md5, truncate_text
from gui.utils import update_progress_bar


def create_folder_structure(service, folder_id, destination, canvas=None, status_label=None):
    """Create the folder structure recursively from Google Drive."""
    if canvas and status_label:
        canvas.itemconfig(status_label, text="Creating folder structure...")
    if not os.path.exists(destination):
        os.makedirs(destination)
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = sorted(results.get('files', []), key=lambda x: x['name'])
    for item in items:
        file_path = os.path.join(destination, item['name'])
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            create_folder_structure(service, item['id'], file_path, canvas, status_label)


def get_all_files(service, folder_id, destination):
    """Recursively get all files and their metadata from Google Drive."""
    files = []
    query = f"'{folder_id}' in parents and trashed=false"
    page_token = None

    while True:
        if page_token:
            results = service.files().list(q=query,
                                           fields="nextPageToken, files(id, name, mimeType, md5Checksum, size)",
                                           pageToken=page_token).execute()
        else:
            results = service.files().list(q=query,
                                           fields="nextPageToken, files(id, name, mimeType, md5Checksum, size)").execute()

        items = sorted(results.get('files', []), key=lambda x: x['name'])
        for item in items:
            file_path = os.path.join(destination, item['name'])
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                files.extend(get_all_files(service, item['id'], file_path))
            else:
                files.append({
                    'id': item['id'],
                    'name': item['name'],
                    'path': file_path,
                    'md5Checksum': item.get('md5Checksum'),
                    'size': int(item['size'])
                })

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return files


def check_existing_files(files, canvas, labels):
    """Check the integrity of existing files."""
    files_to_download = []
    total_files = len(files)

    for idx, file in enumerate(files):
        if os.path.exists(file['path']):
            downloaded_md5 = calculate_md5(file['path'])
            if downloaded_md5 != file['md5Checksum']:
                files_to_download.append(file)
            else:
                canvas.itemconfig(labels['status_label'], text="Verifying")
                canvas.itemconfig(labels['total_progress_label'], text=f"{idx + 1}/{total_files}")
        else:
            files_to_download.append(file)

        update_progress_bar((idx + 1) / total_files, is_verification=True, canvas=canvas)

    canvas.itemconfig(labels['status_label'], text=f"Files to download: {len(files_to_download)}")
    return files_to_download


def download_file(service, file, canvas, labels, pause_event, stop_event):
    """Download a file from Google Drive and verify its checksum."""
    request = service.files().get_media(fileId=file['id'])
    fh = io.FileIO(file['path'], 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    downloaded_size = 0
    start_time = time.time()

    canvas.itemconfig(labels['status_label'], text="Downloading")
    canvas.itemconfig(labels['current_file_label'], text=truncate_text(file['name']))

    while not done:
        if pause_event.is_set():
            canvas.itemconfig(labels['status_label'], text="Download paused")
            pause_event.wait()
            canvas.itemconfig(labels['status_label'], text="Download resumed")
        if stop_event.is_set():
            canvas.itemconfig(labels['status_label'], text="Download stopped")
            return False

        status, done = downloader.next_chunk()
        if status:
            downloaded_size = status.resumable_progress
            speed = downloaded_size / (time.time() - start_time)
            canvas.itemconfig(labels['current_file_progress_label'],
                              text=f"{(downloaded_size / file['size']) * 100:.2f}% ({speed / (1024 * 1024):.2f} MB/s)")
            update_progress_bar(downloaded_size / file['size'], canvas=canvas)

    downloaded_md5 = calculate_md5(file['path'])
    if downloaded_md5 != file['md5Checksum']:
        canvas.itemconfig(labels['status_label'],
                          text=f'Checksum mismatch for {file["path"]}: expected {file["md5Checksum"]}, got {downloaded_md5}')
        os.remove(file['path'])
        return False
    canvas.itemconfig(labels['status_label'], text=f"Downloaded {file['name']}")
    return True


def download_files(service, files_to_download, canvas, labels, pause_event, stop_event):
    """Download all files."""
    total_files = len(files_to_download)
    for idx, file in enumerate(files_to_download):
        if not download_file(service, file, canvas, labels, pause_event, stop_event):
            canvas.itemconfig(labels['status_label'], text=f'Retrying download of {file["path"]}')
            download_file(service, file, canvas, labels, pause_event, stop_event)
        canvas.itemconfig(labels['total_progress_label'], text=f"{idx + 1}/{total_files}")
        percentage = (idx + 1) / total_files * 100
        canvas.itemconfig(labels['total_percentage_label'], text=f"{percentage:.0f}%")
        update_progress_bar((idx + 1) / total_files, canvas=canvas)
    canvas.itemconfig(labels['status_label'], text="Completed download of all files")
