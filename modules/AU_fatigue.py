import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime, time


# AUデータフレームのクレンジング
# タイムスタンプとAUのみ
def editAUdata(file_name: str, file_directory) :
    df = pd.read_csv(f"./output/{file_directory}/{file_name}.csv")
    print(file_name)
    
    # 無関係な行の削除
    df = df[(df[" success"] == 0) | (df[" success"] == 1)]

    # 成功率チェック
    num_of_row = df.shape[0]
    success = np.array(df[" success"])
    count_success = success.sum()
    print(count_success, num_of_row)
    success_rate = count_success/num_of_row*100
    print(f"success rate: {success_rate:.2f}%")
    
    if success_rate == 100 :
        AUR_start = df.columns.get_loc(" AU01_r")
        AUR_end = df.columns.get_loc(" AU45_r")
        timestamp = df.columns.get_loc(" timestamp")
        
        AU_df = df.iloc[:, AUR_start:AUR_end+1]
        time_df = df.iloc[:, timestamp]
        df = pd.concat([time_df, AU_df], axis=1)
        return df, True
    else :
        print("This Video is not appropriate to analyze Action Unit")
        return df, False

# 評価テスト回答結果のデータフレーム化
def my_fatigue(file_name: str) :
    fatigue_file = glob.glob(f"./output/*評価テスト回答.csv")
    fatigue_df = pd.read_csv(fatigue_file[0])
    fatigue_df["タイムスタンプ"] = pd.to_datetime(fatigue_df["タイムスタンプ"])
    
    # 指定日付の構文解析
    date_str = file_name[-14:]
    date = datetime.strptime(f"{date_str}", "%Y%m%d%H%M%S")
    today = date.date()
    is_am = date.time() <= time(12, 0, 0)
    
    # 日付検索
    fatigue_df = fatigue_df[fatigue_df["タイムスタンプ"].dt.strftime("%Y-%m-%d") == str(today)]
    # 午前・午後の判定
    if is_am :
        fatigue_df = fatigue_df[fatigue_df["タイムスタンプ"].dt.time <= time(12, 0, 0)]
        print(date, "am")
    else :
        fatigue_df = fatigue_df[fatigue_df["タイムスタンプ"].dt.time >= time(12, 0, 0)]
        print(date,"pm")
    
    if not fatigue_df.empty :
        return fatigue_df, True
    else :
        return fatigue_df, False

# 主観疲労度の群別スコア算出
def fatigue_group_score(fatigue_df: pd.DataFrame) :
    group_nums = [[10, 13, 14, 17, 21], [2, 5, 15, 18, 20], [1, 4, 6, 9, 12], [8, 11, 19, 23, 25], [3, 7, 16, 22, 24]]
    group_scores = [0] * 5

    print(fatigue_df.shape)
    for i in range(5) :
        for j in range(5):
            group_scores[i] += (fatigue_df.iloc[0, group_nums[i][j]+1 ])
    
    return group_scores

def exec_analysis(file_directory) :
    if not os.path.exists(f"./result/{file_directory}") :
        os.makedirs(f"./result/{file_directory}")

    AU_files = glob.glob(f"./output/{file_directory}/VID*.csv")

    AU_files = [os.path.splitext(os.path.basename(x))[0] for x in AU_files] 
    output_df = pd.DataFrame([], columns=["Video_name", 
                                "group1", "group2", "group3", "group4", "group5", 
                                "q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12","q13","q14","q15","q16","q17","q18","q19","q20","q21","q22","q23","q24","q25",
                                "means_AU01", "means_AU02", "means_AU04", "means_AU05", "means_AU06", "means_AU07", "means_AU09", "means_AU10", "means_AU12", "means_AU14", "means_AU15", "means_AU17", "means_AU020", "means_AU23", "means_AU25", "means_AU26", "means_AU45",
                                "varAU01", "varAU02", "varAU04", "varAU05", "varAU06", "varAU07", "varAU09", "varAU10", "varAU12", "varAU14", "varAU15", "varAU17", "varAU020", "varAU23", "varAU25", "varAU26", "varAU45",
                                "maxAU01", "maxAU02", "maxAU04", "maxAU05", "maxAU06", "maxAU07", "maxAU09", "maxAU10", "maxAU12", "maxAU14", "maxAU15", "maxAU17", "maxAU020", "maxAU23", "maxAU25", "maxAU26", "maxAU45"]
                                , index=range(len(AU_files)))

    for i in range(len(AU_files)) :
        print(output_df.head())
        AU_df, isSuccess = editAUdata(AU_files[i], file_directory)
        fatigue_df, isEmpty = my_fatigue(AU_files[i])
        if (not isSuccess or not isEmpty) :
            output_list = [AU_files[i]] + ["Nan"] * (len(output_df.columns)-1) 
            output_series = pd.Series(output_list)
            output_df.iloc[i, :] = output_series
            continue

        
        fig = plt.figure(figsize=(10,5))
        axes = fig.subplots(1,2)
        bar_list = range(len(fatigue_df.columns))

        """
        axes[0].plot(AU_df.loc[:, " timestamp"], AU_df.loc[:, " AU01_r"])
        for k in range(25) :
            axes[1].bar(f"{bar_list[k+1]}", fatigue_df.iloc[0, k+2], color="blue")
        axes[1].set_ylim(0, 5)

        # plt.show()
        """

        print("fatigue group-scores")
        group_scores = fatigue_group_score(fatigue_df)
        for n in range(len(group_scores)) :
            print(f"group {n}: {group_scores[n]}")
            
        
        q_list = list(fatigue_df.iloc[0, 2:])

        print("means")
        print(AU_df.mean())
        AU_mean_list = list(AU_df.iloc[:, 1:].mean())

        print("var")
        print(AU_df.var())
        AU_var_list = list(AU_df.iloc[:, 1:].var())

        print("max")
        print(AU_df.max())
        AU_max_list = list(AU_df.iloc[:, 1:].max())
        
        output_list = [AU_files[i]] + group_scores + q_list +  AU_mean_list + AU_var_list + AU_max_list
        print(len(output_list))
        output_series = pd.Series(output_list)
        
        output_df.iloc[i, :] = output_series
        
    output_df.to_csv(f"./result/{file_directory}/AU_fatigue_statics.csv", index=False)
    
exec_analysis("250716")