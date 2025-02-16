import os
import sys
import base64
import json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from SmartCamera import ObjectDetectionTop
from SmartCamera import BoundingBox
from SmartCamera import BoundingBox2d

if __name__ == '__main__':

    inference_dir = './inferences'      # 変換元フォルダのパス
    metadata_dir = './inferences_json'  # 変換先フォルダのパス（無ければ新規に作成する）
    
    # metadata フォルダが存在しない場合、作成します
    os.makedirs(metadata_dir, exist_ok=True)

    # Process all inference result files in the inference_dir
    for inf_file in os.listdir(inference_dir):
        inf_path = os.path.join(inference_dir, inf_file)
        
        # Read one file in the folder.
        with open(inf_path, 'r', encoding='utf-8') as json_file:
            buf = json.load(json_file)
        
        # Base64 decode the string in the file.
        if 'O' in buf['Inferences'][0]:
            buf_decode = base64.b64decode(buf['Inferences'][0]['O'])
        else:
            # If no base64 data, just write the file as is
            with open(f'{metadata_dir}/decoded_{inf_file.split(".")[0]}.json', 'w', encoding='utf-8') as file:
                json.dump(buf, file, ensure_ascii=False, indent=4)
        
        # Deserialize the Base64-decoded string.
        ppl_out = ObjectDetectionTop.ObjectDetectionTop.GetRootAsObjectDetectionTop(buf_decode, 0)
        obj_data = ppl_out.Perception()
        res_num = obj_data.ObjectDetectionListLength()

        # Store the deserialized data in json format.
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

        # Output the modified JSON to the metadata folder
        with open(f'{metadata_dir}/{inf_file.split(".")[0]}.json', 'w', encoding='utf-8') as file:
            json.dump(buf, file, ensure_ascii=False, indent=4)
