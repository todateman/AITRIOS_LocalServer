import os
import sys
import base64
import json
import argparse
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from SmartCamera import ObjectDetectionTop
from SmartCamera import BoundingBox
from SmartCamera import BoundingBox2d

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
    ppl_out = ObjectDetectionTop.ObjectDetectionTop.GetRootAsObjectDetectionTop(buf_decode, 0)
    obj_data = ppl_out.Perception()
    res_num = obj_data.ObjectDetectionListLength()

    # デコードしたデータを JSON に変換する
    buf['Inferences'][0].pop('O')
    
    for i in range(res_num):
        obj_list = obj_data.ObjectDetectionList(i)
        union_type = obj_list.BoundingBoxType()
        if union_type == BoundingBox.BoundingBox.BoundingBox2d:
            bbox_2d = BoundingBox2d.BoundingBox2d()
            bbox_2d.Init(obj_list.BoundingBox().Bytes, obj_list.BoundingBox().Pos)
            buf['Inferences'][0][str(i + 1)] = {}
            buf['Inferences'][0][str(i + 1)]['C'] = obj_list.ClassId()
            buf['Inferences'][0][str(i + 1)]['P'] = obj_list.Score()
            buf['Inferences'][0][str(i + 1)]['X'] = bbox_2d.Left()
            buf['Inferences'][0][str(i + 1)]['Y'] = bbox_2d.Top()
            buf['Inferences'][0][str(i + 1)]['x'] = bbox_2d.Right()
            buf['Inferences'][0][str(i + 1)]['y'] = bbox_2d.Bottom()

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
