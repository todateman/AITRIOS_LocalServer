# https://developer.aitrios.sony-semicon.com/edge-ai-sensing/documents/external-transfer-settings-tutorial-for-http-server?version=2025-02-03&progLang=
# $ uvicorn webapp:app_ins --reload --host 127.0.0.1 --port 51797 --no-access-log

from fastapi import FastAPI, Request, status
import os.path
import traceback
import logging

SAVE_PATH_IMG = './images'
SAVE_PATH_META = './inferences'

app_ins = FastAPI()
# Log format
log_format = '%(asctime)s - %(message)s'
# Set log level to INFO
logging.basicConfig(format=log_format, level=logging.INFO)

def save_file(file_type, content, filename):
        file_path = os.path.join(file_type, filename)
        with open(file_path, 'wb') as w_fp:
                w_fp.write(content)


@app_ins.put("/inferences/{filename}")
async def update_items(filename, request: Request):
        try:
                content = await request.body()
                os.makedirs(SAVE_PATH_META, exist_ok=True)
                save_file(SAVE_PATH_META, content, filename)
                logging.info("Meta File Saved: %s", filename)
                return {"status":status.HTTP_200_OK}
        except (Exception):
                traceback.print_exc()


@app_ins.put("/images/{filename}")
async def update_items(filename, request: Request):
        try:
                content = await request.body()
                os.makedirs(SAVE_PATH_IMG, exist_ok=True)
                save_file(SAVE_PATH_IMG, content, filename)
                logging.info("Image File Saved: %s", filename)
                return {"status":status.HTTP_200_OK}
        except (Exception):
                traceback.print_exc()