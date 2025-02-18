# python send_mqtt_message.py -j ./mqtt_json/start.json -b localhost -p 1883 -t "v1/devices/me/rpc/request/11111111"
# python send_mqtt_message.py -j ./mqtt_json/stop.json -b localhost -p 1883 -t "v1/devices/me/rpc/request/22222222"

import json
import paho.mqtt.client as mqtt
import argparse
import os

def send_mqtt_message(broker, port, topic, json_data):
    # MQTTクライアントの設定
    client = mqtt.Client()

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

def main():
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description="MQTTメッセージを送信するツール")
    parser.add_argument('-j', '--json', required=True, help="送信するJSONファイルのパス")
    parser.add_argument('-b', '--broker', default="localhost", help="MQTT Brokerのホスト（デフォルトはlocalhost）")
    parser.add_argument('-p', '--port', type=int, default=1883, help="MQTT Brokerのポート（デフォルトは1883）")
    parser.add_argument('-t', '--topic', required=True, help="送信先のMQTTトピック")

    args = parser.parse_args()

    # JSONファイルの読み込み
    json_data = load_json_file(args.json)

    # JSONデータを送信
    send_mqtt_message(args.broker, args.port, args.topic, json.dumps(json_data))

if __name__ == '__main__':
    main()