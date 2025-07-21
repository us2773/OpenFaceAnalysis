import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy.signal import savgol_filter

file_directory = "output/250707-2"
#file_name = "VID20250701164140"

files = glob.glob(f"./{file_directory}/*.csv")
#print(files)
files = [os.path.splitext(os.path.basename(x))[0] for x in files]
#print(files)

def get_AU_peak(file_name) :
    print(file_name)
    df = pd.read_csv(f"./{file_directory}/{file_name}.csv")
    #print(df.head())

    #print(list(df.columns))

    df = df[(df[" success"] == 0) | (df[" success"] == 1)]
    #print(df.iloc[200, :])

    num_of_row = df.shape[0]
    success = np.array(df[" success"])
    #print(success)
    count_success = success.sum()
    print(count_success, num_of_row)
    print(f"success rate: {(count_success/num_of_row*100):.2f}%")

    au_col = " AU01_r"
    signal = df[au_col].values
    times = df[" timestamp"].values

    # 平滑化（ノイズ除去）
    smoothed = savgol_filter(signal, window_length=7, polyorder=2)

    # 極大値（AU強度ピーク）を検出
    #peaks, _ = find_peaks(smoothed, height=0.1, distance=5)  # height調整で検出感度変更
    
    smoothed = pd.Series(signal).rolling(window=15, center=True).mean().values

    # 可視化
    plt.figure(figsize=(12, 5))
    plt.plot(times, signal, label="Original")
    #plt.plot(times, smoothed, label="Smoothed", linestyle='--')
    #plt.scatter(times[peaks], smoothed[peaks], color='red', label='Expression Peaks')
    #plt.plot(times, smoothed, label=f"Moving Avg)", color='red')
    plt.title("AU01: transition")
    plt.xlabel("Timestamp (s)")
    plt.ylabel("AU Strength")
    #plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    output_path = f"./{file_directory}/AU01"
    if not os.path.exists(output_path) :
        os.makedirs(output_path)
    plt.savefig(f"{output_path}/{file_name}_AU_transition.png", bbox_inches="tight")
    #plt.show()
    
for i in range(len(files)):
    get_AU_peak(files[i])