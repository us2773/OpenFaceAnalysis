import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from statsmodels.nonparametric.smoothers_lowess import lowess



file_directory = "250716"
#file_name = "VID20250701164140"

files = glob.glob(f"./output/{file_directory}/VID*.csv")
#print(files)
files = [os.path.splitext(os.path.basename(x))[0] for x in files]
#print(files)


def get_AU_noise(file_name) :
    print(file_name)
    df = pd.read_csv(f"./output/{file_directory}/{file_name}.csv")

    df = df[(df[" success"] == 0) | (df[" success"] == 1)]

    num_of_row = df.shape[0]
    success = np.array(df[" success"])
    count_success = success.sum()
    print(count_success, num_of_row)
    print(f"success rate: {(count_success/num_of_row*100):.2f}%")

    au_col = " AU01_r"
    
    trend_est = lowess(df[au_col], df[" timestamp"], frac=0.1, return_sorted=False)
    
    # 残差（不規則変動成分）
    residual = df[au_col] - trend_est
    df[f"{au_col}_trend"] = trend_est
    df[f"{au_col}_fluct"] = residual
    
    mean = df[f"{au_col}_fluct"].mean()
    print(f"mean: {mean}")
    var = df[f"{au_col}_fluct"].var()
    print(f"var: {var}")
    std = df[f"{au_col}_fluct"].std()
    print(f"cv: {std / mean}")
    
    # 可視化
    plt.figure(figsize=(10, 4))
    plt.plot(df[" timestamp"], df[f"{au_col}"], label="Original")
    #plt.show()
    plt.plot(df[" timestamp"], df[f"{au_col}_trend"], label="Trend (LOWESS)", color="green")
    #plt.show()
    plt.plot(df[" timestamp"], df[f"{au_col}_fluct"], label="Residual (Fluctuation)", color="red", linestyle="--")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel(f"{au_col}")
    plt.title(f"{au_col}: Trend and Fluctuation")
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"./result/{file_directory}/{file_name}_{au_col}_trend_noise.png", bbox_inches="tight")
    

for i in range(len(files)):
    get_AU_noise(files[i])


#get_AU_noise("VID_20250707163518_bangsup_f2")