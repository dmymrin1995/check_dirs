import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DownloadedFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.ready_flag = False
        self.ready_file_path = ""

    def on_created(self, event):
        if not event.is_directory and not event.src_path.lower().endswith(".tmp"):
            print(f"Загружен новый файл: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory and not event.src_path.lower().endswith(".tmp"):
            print(f"Файл изменен: {event.src_path}")
            self.ready_flag = True
            self.ready_file_path = event.src_path

    def is_ready(self):
        return self.ready_flag, self.ready_file_path


def track_downloaded_files(directory_to_track):
    event_handler = DownloadedFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_track, recursive=False)
    observer.start()

    try:
        while True:
            flag, file_path = event_handler.is_ready()

            if flag and file_path.endswith(".pdf"):
                print(f"Файл готов: {flag} путь к файлу: {file_path}")

                ##
                ##

                event_handler.ready_flag = False
                event_handler.ready_file_path = ""
                break

            time.sleep(1)

            print(f"Файл готов: {flag} путь к файлу: {file_path}")

    except KeyboardInterrupt:
        observer.stop()
        observer.join()


directory_to_track = r"c:\Users\dmymrin1995\Downloads"
track_downloaded_files(directory_to_track)
