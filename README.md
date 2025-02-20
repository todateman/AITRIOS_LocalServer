# AITRIOS LocalEdition HTTP Server

AITRIOS LocalConsoleに代わる推論結果のメタデータ・画像データの受信、推論結果のメタデータの変換、推論開始・停止の処理を行うファイル群です。

## send_mqtt_message.py

AITRIOS LocalEditionのデバイス向けにMQTT MessageをPublishします。

```send_mqtt_message.py```は次のようにオプション付きで実行してください。

```bash
python send_mqtt_message.py -j ./mqtt_json/start.json -b localhost -p 1883 -t "v1/devices/me/rpc/request/11111111"
```

* -j : 送信するMessageを記載したJSONファイルのパスを相対パスもしくは絶対パスで指定してください。
  * ./mqtt_json/start.json : 推論開始のMessageを記載したJSONファイルです。<br>
    StorageNameとStorageNameIRでそれぞれ推論結果のメタデータと画像データの送信先のhttpサーバを指定してください。
  * ./mqtt_json/stop.json  : 推論停止のMessageを記載したJSONファイルです。
* -b : MQTT Brokerのホストを指定してください。（デフォルトはlocalhost）
* -p : MQTT Brokerのポートを指定してください。（デフォルトは1883）
* -t : 送信先のMQTTトピックを指定してください。（指定がない場合はデフォルトトピックとして"v1/devices/me/rpc/request/<ランダムな8桁の数字>"が使用されます）


## show_inferences_monitoring.py

推論結果のJSONファイルの生成を監視し、後述の```show_inferences.py```を自動で実行します。

```show_inferences_monitoring.py```は次のようにオプション付きで実行してください。

```bash
python show_inferences_monitoring.py -j inferences_json -g images -s inferences_images
```

* -j : 推論結果が格納されているJSONファイルの保存先ディレクトリを相対パスもしくは絶対パスで指定してください。
* -g : 背景画像ファイル（JPEG形式）の保存先ディレクトリを相対パスもしくは絶対パスで指定してください。
* -s : 画像の保存先ディレクトリを相対パスもしくは絶対パスで指定してください。


## show_inferences.py

推論結果のメタデータのJSONファイルを図として表示・保存します。

```show_inferences.py```は次のようにオプション付きで実行してください。

**プレビューせず保存する場合**

```bash
python show_inferences.py -j ./inferences_json/20250216144204887.json -g ./images/20250216144204887.jpg -s ./output/output_image.png
```

**保存せずプレビューのみする場合**

```bash
python show_inferences.py -j ./inferences_json/20250216144204887.json -g ./images/20250216144204887.jpg
```

* -j : 推論結果が格納されているJSONファイルのパスを相対パスもしくは絶対パスで指定してください。
* -g : 背景画像ファイル（JPEG形式）のパスを相対パスもしくは絶対パスで指定してください。
* -s : 画像を保存するパスを相対パスもしくは絶対パスで指定してください。指定した場合、プレビューは表示されません


## webapp.py
[外部転送設定チュートリアル（HTTPサーバー用）](https://developer.aitrios.sony-semicon.com/edge-ai-sensing/documents/external-transfer-settings-tutorial-for-http-server?version=2025-02-03&progLang=)を参考に、推論結果のメタデータ・画像データの受信を行うhttpサーバ機能を実行します。<br>
また、推論結果のメタデータを保存すると自動的に次項で紹介する```./Classification_json/Classification_json.py```もしくは```./Detection_json/Detection_json.py```を実行します。<br>
どちらを実行するかはソースコード内のコメントアウトで切り替えてください。

```webapp.py```は次のように実行してください。

```bash
uvicorn webapp:app_ins --reload --host 127.0.0.1 --port 62073 --no-access-log
```

## ./Classification_json/Classification_json.py

クラス分類の推論結果のメタデータをデシリアイズします。

次のように実行してください。

**一括で処理する場合**

```bash
python ./Classification_json/Classification_json.py -i ./inferences/ -o ./inferences_json
```

**単体のファイルを処理する場合**

```bash
python ./Classification_json/Classification_json.py -f ./inferences/20250216144204887.txt -o ./inferences_json
```

* -i : 処理対象の入力ファイルの存在するディレクトリを相対パスもしくは絶対パスで指定してください。<br>
       ディレクトリ内のファイルは一括で処理されます。
* -o : 処理後の出力ファイルの保存先ディレクトリを相対パスもしくは絶対パスで指定してください。
* -f : 処理対象の入力ファイルを相対パスもしくは絶対パスで指定してください。<br>
       この場合、単体のファイルのみを処理します。

## ./Detection_json/Detection_json.py

物体検出の推論結果のメタデータをデシリアイズします。

次のように実行してください。

**一括で処理する場合**

```bash
python ./Detection_json/Detection_json.py -i ./inferences/ -o ./inferences_json
```

**単体のファイルを処理する場合**

```bash
python ./Detection_json/Detection_json.py -f ./inferences/20250216144204887.txt -o ./inferences_json
```

* -i : 処理対象の入力ファイルの存在するディレクトリを相対パスもしくは絶対パスで指定してください。<br>
       ディレクトリ内のファイルは一括で処理されます。
* -o : 処理後の出力ファイルの保存先ディレクトリを相対パスもしくは絶対パスで指定してください。
* -f : 処理対象の入力ファイルを相対パスもしくは絶対パスで指定してください。<br>
       この場合、単体のファイルのみを処理します。
