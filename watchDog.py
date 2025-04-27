import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, filepath):
        self.filepath = filepath
        self.process = subprocess.Popen(['python', self.filepath])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("File changed, reloading...")
            self.process.kill()
            self.process = subprocess.Popen(['python', self.filepath])

if __name__ == "__main__":
    target = "mainUI.py"  # <-- thay bằng file chính của bạn
    event_handler = ReloadHandler(target)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
