# https://developer.aitrios.sony-semicon.com/edge-ai-sensing/documents/external-transfer-settings-tutorial-for-http-server?version=2025-02-03&progLang=
# $ uvicorn webapp:app_ins --reload --host 127.0.0.1 --port **** --no-access-log

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
from fastapi import FastAPI, Request, status, BackgroundTasks
import os.path
import traceback
import logging
import threading

SAVE_PATH_IMG = './images'
SAVE_PATH_META = './inferences'

app_ins = FastAPI()
# Log format
log_format = '%(asctime)s - %(message)s'
# Set log level to INFO
logging.basicConfig(format=log_format, level=logging.INFO)

# Ensure the required directories exist
os.makedirs(SAVE_PATH_IMG, exist_ok=True)  # Create 'images' folder if it doesn't exist
os.makedirs(SAVE_PATH_META, exist_ok=True)  # Create 'inferences' folder if it doesn't exist

def save_file(file_type, content, filename):
        file_path = os.path.join(file_type, filename)
        with open(file_path, 'wb') as w_fp:
                w_fp.write(content)

@app_ins.put("/inferences/{filename}")
async def update_items(filename, request: Request):
        try:
                content = await request.body()
                save_file(SAVE_PATH_META, content, filename)
                logging.info("Meta File Saved: %s", filename)
                return {"status":status.HTTP_200_OK}
        except (Exception):
                traceback.print_exc()

@app_ins.put("/images/{filename}")
async def update_items(filename, request: Request):
        try:
                content = await request.body()
                save_file(SAVE_PATH_IMG, content, filename)
                logging.info("Image File Saved: %s", filename)
                return {"status":status.HTTP_200_OK}
        except (Exception):
                traceback.print_exc()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        # If a file is added to the 'inferences' folder, execute Detection_json.py
        if event.src_path.endswith('.txt'):  # Assuming the inference files are .txt
            logging.info(f"New file detected: {event.src_path}")
            time.sleep(1)  # Give some time to ensure the file is completely written
            subprocess.run(['python', './Detection_json/Detection_json.py'])  # Use the full path to the script

def start_watching():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, SAVE_PATH_META, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keeps the watcher running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Background task function to start the watchdog observer
@app_ins.on_event("startup")
async def start_watchdog():
    # Start the file watcher in a background thread
    watcher_thread = threading.Thread(target=start_watching)
    watcher_thread.daemon = True
    watcher_thread.start()