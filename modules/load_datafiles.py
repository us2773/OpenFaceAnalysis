import os
import glob
import numpy as np
import pandas as pd

def check_result_directory(file_directory: str) :
    # 結果出力ディレクトリの存在チェック
    if not os.path.exists(f"./result/{file_directory}") :
        os.makedirs(f"./result/{file_directory}")
        
def get_file_names(file_directory):
    # ファイル名の全取得
    files = glob.glob(f"./output/{file_directory}/*.csv")
    files = [os.path.splitext(os.path.basename(x))[0] for x in files]

def check_success_rate(df: pd.DataFrame) :
    # 無関係なデータ行削除
    try :
        df = df[(df[" success"] == 0) | (df[" success"] == 1)]
        
        # 成功率チェック
        num_of_row = df.shape[0]
        successes = np.array(df[" success"])
        count_success = successes.sum()
        success_rate = (count_success/num_of_row*100)
        print(f"success rate: {success_rate:.2f}%")
        return success_rate
    except KeyError:
        return 0
    
def check_confidence(df: pd.DataFrame) :
    # 最長信頼区間の計算
    confidence_list = list(df.loc[:, " confidence"])
    confidence_length_max = 0
    confidence_offset = 0
    length_count = 0
    offset_now = 0
    
    for i in range(len(confidence_list)) :        
        if confidence_list[i] >= 0.80 :
                length_count += 1
        else :
            if confidence_length_max < length_count :
                confidence_length_max = length_count
                confidence_offset = offset_now
                offset_now = i+1
                
            length_count = 0
    if confidence_length_max < length_count :
        confidence_length_max = length_count  
                    
    print(f"max frames length that confidence is enough: {confidence_length_max}/{len(confidence_list)}")
    return {"confidence_length_max": confidence_length_max, "confidence_offset": confidence_offset}
