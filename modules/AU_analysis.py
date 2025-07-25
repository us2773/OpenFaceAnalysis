import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess


# AUデータ抽出・プロット化
def AUs_plot(df: pd.DataFrame, plot_num: int) -> plt.figure:
    fig = plt.figure(figsize=(12,8))
    AUR_start = df.columns.get_loc(" AU01_r")
    AUR_end = df.columns.get_loc(" AU45_r")
    
    if plot_num == 17 :
        axes = fig.subplots(5, 4)
        # plt.suptitle(file_name)
        for i in range(AUR_end - AUR_start+1) :
            axes[i//4][i%4].plot(df.loc[:, " timestamp"], df.iloc[:, AUR_start+i])
            axes[i//4][i%4].set_title(df.columns.values[AUR_start+i])
            fig.subplots_adjust(hspace=0.5, wspace=0.5)
    
    elif 0 <= plot_num < 17 :
        axes = fig.subplots()
        axes.plot(df.loc[:, " timestamp"], df.iloc[:, AUR_start+plot_num])

    # fig.savefig(f"./result/{file_directory}/{file_name}.png", bbox_inches="tight")
    # fig.show()
    return fig
    # fig.clf()
    
# AUをノイズとトレンドに分離する関数
def AU_trend_noise(df: pd.DataFrame, plot_num: int) :

    # AU種類指定
    # au_col = " AU01_r"
    AUR_start = df.columns.get_loc(" AU01_r")
    
    # LOWESS局所回帰によるトレンド抽出
    AUR_moving = df.iloc[:, AUR_start+plot_num]
    AUR_name = df.columns(AUR_start+plot_num)
    trend_est = lowess(AUR_moving, df.iloc[:, AUR_start+plot_num], df[" timestamp"], frac=0.1, return_sorted=False)
    
    # 残差（不規則変動成分）
    residual = AUR_moving - trend_est
    df[f"{AUR_name}_trend"] = trend_est
    df[f"{AUR_name}_fluct"] = residual
    
    # 基本統計値の算出
    mean = df[f"{AUR_name}_fluct"].mean()
    print(f"mean: {mean}")
    var = df[f"{AUR_name}_fluct"].var()
    print(f"var: {var}")
    std = df[f"{AUR_name}_fluct"].std()
    print(f"cv: {std / mean}")
    
    # プロット化・保存
    plt.figure(figsize=(10, 4))
    plt.plot(df[" timestamp"], df[f"{AUR_name}"], label="Original")
    plt.plot(df[" timestamp"], df[f"{AUR_name}_trend"], label="Trend (LOWESS)", color="green")
    plt.plot(df[" timestamp"], df[f"{AUR_name}_fluct"], label="Residual (Fluctuation)", color="red", linestyle="--")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel(f"{AUR_name}")
    plt.title(f"{AUR_name}: Trend and Fluctuation")
    plt.tight_layout()
    # plt.savefig(f"./result/{file_directory}/{file_name}_{au_col}_trend_noise.png", bbox_inches="tight")