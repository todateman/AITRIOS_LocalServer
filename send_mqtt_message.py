# python send_mqtt_message.py -j ./mqtt_json/start.json -b localhost -p 1883 -t "v1/devices/me/rpc/request/11111111"
# python send_mqtt_message.py -j ./mqtt_json/stop.json -b localhost -p 1883 -t "v1/devices/me/rpc/request/22222222"

import random
import json
from paho.mqtt import client as mqtt_client
import argparse
import os

def send_mqtt_message(broker, port, topic, json_data, client_id):
    # MQTTクライアントの設定
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    
    client.on_connect = on_connect

    # MQTT Brokerへの接続
    client.connect(broker, port)

    # メッセージの送信
    client.publish(topic, json_data)

    # メッセージ送信後に接続を切断
    client.disconnect()

    print(f"Message sent to topic {topic}")

def load_json_file(file_path):
    # JSONファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_default_topic():
    # トピックの末尾にランダムな8桁の数字を生成
    return f"v1/devices/me/rpc/request/{random.randint(10000000, 99999999)}"

def main():
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description="MQTTメッセージを送信するツール")
    parser.add_argument('-j', '--json', required=True, help="送信するJSONファイルのパス")
    parser.add_argument('-b', '--broker', default="localhost", help="MQTT Brokerのホスト（デフォルトはlocalhost）")
    parser.add_argument('-p', '--port', type=int, default=1883, help="MQTT Brokerのポート（デフォルトは1883）")
    parser.add_argument('-t', '--topic', help="送信先のMQTTトピック（指定がない場合はデフォルトトピックが使用されます）")

    args = parser.parse_args()
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    # トピックが指定されていない場合、デフォルトトピックを生成
    topic = args.topic if args.topic else generate_default_topic()

    # JSONファイルの読み込み
    json_data = load_json_file(args.json)

    # JSONデータを送信
    send_mqtt_message(args.broker, args.port, topic, json.dumps(json_data), client_id)

if __name__ == '__main__':
    main()
