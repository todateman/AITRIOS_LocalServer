import os
import sys
import base64
import json
import argparse
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from SmartCamera import ClassificationTop

def process_file(inf_path, metadata_dir):
    # JSON ファイルを読み込む
    with open(inf_path, 'r', encoding='utf-8') as json_file:
        buf = json.load(json_file)
    
    # Base64 データが含まれている場合、デコードする
    if 'O' in buf['Inferences'][0]:
        buf_decode = base64.b64decode(buf['Inferences'][0]['O'])
    else:
        # Base64 データが含まれていない場合、デコードしない
        with open(f'{metadata_dir}/decoded_{os.path.basename(inf_path).split(".")[0]}.json', 'w', encoding='utf-8') as file:
            json.dump(buf, file, ensure_ascii=False, indent=4)
    
    # Base64 でデコードされた文字列をデシリアライズ化する
    ppl_out = ClassificationTop.ClassificationTop.GetRootAsClassificationTop(buf_decode, 0)
    cls_data = ppl_out.Perception()
    res_num = cls_data.ClassificationListLength()

    # デコードしたデータを JSON に変換する
    buf['Inferences'][0].pop('O')
    for i in range(res_num):
        cls_list = cls_data.ClassificationList(i)
        buf['Inferences'][0][str(i + 1)] = {}
        buf['Inferences'][0][str(i + 1)]['class_id'] = cls_list.ClassId()
        buf['Inferences'][0][str(i + 1)]['score'] = round(cls_list.Score(), 6)

    # JSONファイルに変換したデータを保存する
    with open(f'{metadata_dir}/{os.path.basename(inf_path).split(".")[0]}.json', 'w', encoding='utf-8') as file:
        json.dump(buf, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process JSON files for object detection.')
    
    # オプションの追加
    parser.add_argument('-i', '--input', type=str, help='Input directory or file (relative or absolute path).')
    parser.add_argument('-o', '--output', type=str, help='Output directory (relative or absolute path).')
    parser.add_argument('-f', '--file', type=str, help='Single input file (relative or absolute path).')

    args = parser.parse_args()

    # デフォルトのディレクトリ
    inference_dir = 'inferences'
    metadata_dir = 'inferences_json'

    # 出力ディレクトリが指定されていれば変更
    if args.output:
        metadata_dir = os.path.abspath(args.output)
    os.makedirs(metadata_dir, exist_ok=True)

    # 入力ディレクトリが指定されていれば変更
    if args.input:
        inference_dir = os.path.abspath(args.input)
    
    # 入力がファイルの場合、そのファイルを処理
    if args.file:
        inf_path = os.path.abspath(args.file)
        process_file(inf_path, metadata_dir)
    
    # 入力がディレクトリの場合、そのディレクトリ内のファイルを処理
    elif os.path.isdir(inference_dir):
        for inf_file in os.listdir(inference_dir):
            inf_path = os.path.join(inference_dir, inf_file)
            if os.path.isfile(inf_path):
                process_file(inf_path, metadata_dir)
    else:
        print(f"指定された入力パスはディレクトリでもファイルでもありません: {inference_dir}")
