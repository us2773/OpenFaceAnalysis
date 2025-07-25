import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

file_directory = "output/250707-2"

# 結果出力ディレクトリのチェック・新規作成
output_path = f"./{file_directory}/AU01"
if not os.path.exists(output_path) :
        os.makedirs(output_path)

# CSVファイル確認
files = glob.glob(f"./{file_directory}/*.csv")
files = [os.path.splitext(os.path.basename(x))[0] for x in files]

# ファイル名を受け取りピーク点付きプロットを返す関数
def get_AU_peak(file_name) :
    print(file_name)
    df = pd.read_csv(f"./{file_directory}/{file_name}.csv")

    # 無関係なデータ行削除
    df = df[(df[" success"] == 0) | (df[" success"] == 1)]

    # 成功率チェック
    num_of_row = df.shape[0]
    success = np.array(df[" success"])
    count_success = success.sum()
    print(count_success, num_of_row)
    print(f"success rate: {(count_success/num_of_row*100):.2f}%")

    # AU種類指定
    au_col = " AU01_r"
    signal = df[au_col].values
    times = df[" timestamp"].values

    # 可視化
    plt.figure(figsize=(12, 5))
    plt.plot(times, signal, label="Original")
    plt.title("AU01: transition")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("AU Strength")
    plt.grid(True)
    plt.tight_layout()
    
    # 保存
    plt.savefig(f"{output_path}/{file_name}_AU_transition.png", bbox_inches="tight")
    
for i in range(len(files)):
    get_AU_peak(files[i])