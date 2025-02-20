# python show_inferences_monitoring.py -j inferences_json -g images -s inferences_images
import subprocess
import os
from watchfiles import watch
import argparse
import sys

inferences_Prg = './show_inferences.py'  # 推論結果のメタデータを表示するプログラム

# アクションタイプを文字列にマッピング
action_type_map = {
    1: "Added",
    2: "Modified",
    3: "Deleted",
}

# 現在のPython環境のパスを取得
python_executable = sys.executable

def watch_folder(folder_path, image_path=None, save_path=None):
    print(f"監視を開始します: {folder_path}")
    # フォルダ内の変更を監視
    for changes in watch(folder_path):
        for action, path in changes:
            # 新しいJSONファイルが追加された場合
            if action_type_map.get(action) == "Added" and path.endswith('.json'):
                print(f"新しいJSONファイルが追加されました: {path}")
                basename_without_ext = os.path.splitext(os.path.basename(path))[0]  # 拡張子を除いたファイル名を取得
                # 画像ファイルのパスと保存先のパスを作成
                full_image_path = os.path.join(image_path, basename_without_ext + '.jpg')
                full_save_path = os.path.join(save_path, basename_without_ext + '.png')

                try:
                    # subprocess.runでshow_inferences_with_save.pyを実行
                    result = subprocess.run(
                        [python_executable, inferences_Prg, '-j', path, '-g', full_image_path, '-s', full_save_path],
                        check=True, capture_output=True, text=True, encoding='utf-8'
                    )
                    print(result.stdout)  # 実行結果を表示
                except subprocess.CalledProcessError as e:
                    print(f"エラーが発生しました: {e}")
                    print(f"エラー内容: {e.stderr}")

if __name__ == "__main__":
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description='JSONファイルからオブジェクト検出結果を表示し、必要に応じて画像として保存します。')
    parser.add_argument('-j', '--json', type=str, required=True, help='推論結果が格納されているJSONファイルのパス')
    parser.add_argument('-g', '--image', type=str, help='背景画像ファイルのパス（JPEG形式）')
    parser.add_argument('-s', '--save', type=str, help='画像を保存するパス')
    args = parser.parse_args()

    # 必要なディレクトリが存在することを確認する
    os.makedirs(args.save, exist_ok=True)  # 画像ファイルの保存先が存在しない場合は作成する

    # 指定されたファイルパスに基づいて関数を実行
    watch_folder(args.json, args.image, args.save)
