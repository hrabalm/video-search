import time

from watchdog.observers import Observer

FOLDERS_TO_WATCH = []
EXTENSIONS = ["mp4", "mkv", "avi", "flv"]


if __name__ == "__main__":
    observer = Observer()
    event_handler = None
    for path in FOLDERS_TO_WATCH:
        observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
