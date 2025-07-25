import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

file_directory = "250716"

# 結果出力ディレクトリのチェック・新規作成
if not os.path.exists(f"./result/{file_directory}") :
        os.makedirs(f"./result/{file_directory}")

# CSVファイル確認
files = glob.glob(f"./output/{file_directory}/VID*.csv")
files = [os.path.splitext(os.path.basename(x))[0] for x in files]

# ファイル名を受け取りAU全種の時系列プロットを返す関数
def getAU(file_name) :
    print(file_name)
    
    df = pd.read_csv(f"./output/{file_directory}/{file_name}.csv")
    print(df.head())

    # 無関係なデータ行削除
    df = df[(df[" success"] == 0) | (df[" success"] == 1)]

    # 成功率チェック
    num_of_row = df.shape[0]
    success = np.array(df[" success"])
    count_success = success.sum()
    print(count_success, num_of_row)
    print(f"success rate: {(count_success/num_of_row*100):.2f}%")

    # AUデータ抽出・プロット化
    fig = plt.figure(figsize=(12,8))
    axes = fig.subplots(5, 4)
    plt.suptitle(file_name)
    
    AUR_start = df.columns.get_loc(" AU01_r")
    AUR_end = df.columns.get_loc(" AU45_r")
    for i in range(AUR_end - AUR_start+1) :
        axes[i//4][i%4].plot(df.loc[:, " timestamp"], df.iloc[:, AUR_start+i])
        axes[i//4][i%4].set_title(df.columns.values[AUR_start+i])

    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    fig.savefig(f"./result/{file_directory}/{file_name}.png", bbox_inches="tight")
    fig.clf()


    # ランドマークの抽出・プロット
    frame_num = 50

    x_cols = [f" X_{i}" for i in range(68)]
    y_cols = [f" Y_{i}" for i in range(68)]

    landmarks_x = df.loc[frame_num, x_cols]
    landmarks_y = df.loc[frame_num, y_cols]
    
    """
    x_cols_pixel = [f" x_{i}" for i in range(68)]
    y_cols_pixel = [f" y_{i}" for i in range(68)]
    landmarks_x_pixel = df.loc[frame_num, x_cols_pixel]
    landmarks_y_pixel = df.loc[frame_num, y_cols_pixel]
    """

    for i in range(len(landmarks_x)) :
        plt.scatter(landmarks_x[i], landmarks_y[i])
        plt.text(landmarks_x[i], landmarks_y[i], f"{i}")
                
    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.title(f"{file_name} landmark mapping")
    plt.savefig(f"./result/{file_directory}/{file_name}_landmarkmapping.png", bbox_inches="tight")
    #plt.show()
    plt.clf()

    # 成功率の時系列プロット
    plt.plot(df.loc[:, " timestamp"], df.loc[:, " success"])
    plt.ylim(-0.1, 1.1)
    plt.title(f"{file_name} success rate(mean: {(count_success/num_of_row*100):.2f}%)")
    plt.savefig(f"./result/{file_directory}/{file_name}_success_rate.png", bbox_inches="tight")
    #plt.show()
    plt.clf()
    
    # 最長信頼区間の計算
    confidence_list = list(df.loc[:, " confidence"])
    confidence_length_max = 0
    count = 0
    for i in range(len(confidence_list)) :        
        if confidence_list[i] >= 0.70 :
                count += 1
        else :
            if confidence_length_max < count :
                confidence_length_max = count  
            count = 0
    if confidence_length_max < count :
        confidence_length_max = count  
                    
    print(f"max frames length that confidence is enough: {confidence_length_max}/{len(confidence_list)}")
    
    # 信頼度と成功率のプロット
    plt.plot(df.loc[:, " timestamp"], df.loc[:, " confidence"], label="confidence")
    plt.bar(df.loc[:, " timestamp"], df.loc[:, " success"], label="success_rate", linewidth=0, color="#ffc0c0", width=0.035)
    plt.legend()
    plt.ylim(-0.1, 1.1)
    plt.title(f"{file_name} landmark-estimation confidence(max_length:{confidence_length_max}/{len(confidence_list)})")
    plt.savefig(f"./result/{file_directory}/{file_name}_landmark_confidence.png", bbox_inches="tight")
    #plt.show()
    plt.clf()
    
# 実行
if __name__ == "__main__" :
    for i in files :
            getAU(i)