import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import matplotlib.image as mpimg

def plot_inferences(file_path, image_path=None, save_path=None):
    # JSONファイルを読み込む
    with open(file_path, 'r') as f:
        data = json.load(f)

    # 推論結果を取得（最初のインファレンスデータ）
    inferences = data['Inferences'][0]  # 複数のインファレンスがある場合、最初のものを利用

    # 図形を描画する準備
    fig, ax = plt.subplots(figsize=(6, 6))

    # 画像パスが指定されていれば、背景画像を表示
    if image_path:
        img = mpimg.imread(image_path)
        ax.imshow(img, extent=[0, 320, 0, 320])  # 画像のサイズをプロットの座標に合わせる

    # 検出されたオブジェクトの情報を使って矩形とテキストを描画
    for key, inference in inferences.items():
        if key == 'T':
            continue  # タイムスタンプは無視

        class_label = inference['C']
        confidence = inference['P']
        x, y, width, height = inference['X'], inference['Y'], inference['x'] - inference['X'], inference['y'] - inference['Y']
        
        # 矩形を追加
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        
        # クラスと信頼度を矩形内にテキストとして追加
        ax.text(x + width / 2, y + height / 2, f"Class: {class_label}\nConf: {confidence:.2f}", 
                color='white', ha='center', va='center', fontsize=8, fontweight='bold', bbox=dict(facecolor='red', alpha=0.5))

    # 軸の範囲とラベルを設定
    ax.set_xlim(0, 320)
    ax.set_ylim(0, 320)  # Y軸を上（0）から下（320）に設定
    ax.set_title("Object Detection Bounding Boxes with Class and Confidence")

    # プレビューとして表示するか、保存するかを決定
    if save_path:
        # 保存先が指定されている場合、画像をファイルとして保存
        plt.savefig(save_path)
    else:
        # 保存先が指定されていない場合は、プレビューとして表示
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

if __name__ == "__main__":
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description='JSONファイルからオブジェクト検出結果を表示し、必要に応じて画像として保存します。')
    parser.add_argument('-j', '--json', type=str, required=True, help='推論結果が格納されているJSONファイルのパス')
    parser.add_argument('-g', '--image', type=str, help='背景画像ファイルのパス（JPEG形式）')
    parser.add_argument('-s', '--save', type=str, help='画像を保存するパス。指定した場合、プレビューは表示されません')
    args = parser.parse_args()

    # 指定されたファイルパスに基づいて関数を実行
    plot_inferences(args.json, args.image, args.save)