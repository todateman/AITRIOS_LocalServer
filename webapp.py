# https://developer.aitrios.sony-semicon.com/edge-ai-sensing/documents/external-transfer-settings-tutorial-for-http-server?version=2025-02-03&progLang=
# $ uvicorn webapp:app_ins --reload --host 127.0.0.1 --port **** --no-access-log

from watchfiles import watch
import subprocess
import time
from fastapi import FastAPI, Request, status, BackgroundTasks
import os.path
import traceback
import logging
import threading

SAVE_PATH_IMG = 'images'                                        # 画像ファイルの保存先
SAVE_PATH_META = 'inferences'                                   # メタデータファイルの保存先
SAVE_PATH_JSON = 'inferences_json'                              # JSON ファイルの保存先
Decode_Prg = './Detection_json/Detection_json.py'               # 物体検出用デコードプログラム
# Decode_Prg = './Classification_json/Classification_json.py'     # 分類用デコードプログラム

# アクションタイプを文字列にマッピング
action_type_map = {
    1: "Added",
    2: "Modified",
    3: "Deleted",
}

app_ins = FastAPI()
# Log format
log_format = '%(asctime)s - %(message)s'
# Set log level to INFO
logging.basicConfig(format=log_format, level=logging.INFO)

# 必要なディレクトリが存在することを確認する
os.makedirs(SAVE_PATH_IMG, exist_ok=True)   # 画像ファイルの保存先が存在しない場合は作成する
os.makedirs(SAVE_PATH_META, exist_ok=True)  # メタデータファイルの保存先が存在しない場合は作成する
os.makedirs(SAVE_PATH_JSON, exist_ok=True)  # JSON ファイルの保存先が存在しない場合は作成する

# ファイルを保存する関数
def save_file(file_type, content, filename):
        file_path = os.path.join(file_type, filename)
        with open(file_path, 'wb') as w_fp:
                w_fp.write(content)

# メタデータファイルを受け取るエンドポイント
@app_ins.put("/inferences/{filename}")
async def update_items(filename, request: Request):
        try:
                content = await request.body()
                save_file(SAVE_PATH_META, content, filename)
                logging.info("Meta File Saved: %s", filename)
                return {"status":status.HTTP_200_OK}
        except (Exception):
                traceback.print_exc()

# 画像ファイルを受け取るエンドポイント
@app_ins.put("/images/{filename}")
async def update_items(filename, request: Request):
        try:
                content = await request.body()
                save_file(SAVE_PATH_IMG, content, filename)
                logging.info("Image File Saved: %s", filename)
                return {"status":status.HTTP_200_OK}
        except (Exception):
                traceback.print_exc()

def monitor_inferences():
    # メタデータファイルの保存先で新しい.txtファイルを監視する
    for changes in watch(SAVE_PATH_META):
        for action, path in changes:
            # アクションタイプが追加の場合
            if action_type_map.get(action) == "Added":
                # ファイルパスの末尾が".txt"の場合
                if path.endswith('.txt'):
                        logging.info("New file detected: %s", path)
                        #time.sleep(1)  # ファイルが完全に書き込まれるまで待機
                        subprocess.run(['python', Decode_Prg, '-f', path, '-o', SAVE_PATH_JSON], capture_output=True, text=True)  # Execute Detection_json.py

# バックグラウンドスレッドでファイル監視を開始する
@app_ins.on_event("startup")
async def start_watchdog():
    # バックグラウンドスレッドでファイル監視を開始する
    watcher_thread = threading.Thread(target=monitor_inferences)
    watcher_thread.daemon = True
    watcher_thread.start()
