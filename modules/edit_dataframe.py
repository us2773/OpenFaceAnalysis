import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

file_directory = "250716"
#file_name = "VID20250701164140"

if not os.path.exists(f"./result/{file_directory}") :
        os.makedirs(f"./result/{file_directory}")


files = glob.glob(f"./output/{file_directory}/VID*.csv")
#print(files)
files = [os.path.splitext(os.path.basename(x))[0] for x in files]
#print(files)

def getAU(file_name) :
    print(file_name)
    df = pd.read_csv(f"./output/{file_directory}/{file_name}.csv")
    print(df.head())

    #print(list(df.columns))

    df = df[(df[" success"] == 0) | (df[" success"] == 1)]
    #print(df.iloc[200, :])

    num_of_row = df.shape[0]
    success = np.array(df[" success"])
    #print(success)
    count_success = success.sum()
    print(count_success, num_of_row)
    print(f"success rate: {(count_success/num_of_row*100):.2f}%")

    AUR_start = df.columns.get_loc(" AU01_r")
    AUR_end = df.columns.get_loc(" AU45_r")

    fig = plt.figure(figsize=(12,8))
    axes = fig.subplots(5, 4)
    plt.suptitle(file_name)
    for i in range(AUR_end - AUR_start+1) :
        axes[i//4][i%4].plot(df.loc[:, " timestamp"], df.iloc[:, AUR_start+i])
        axes[i//4][i%4].set_title(df.columns.values[AUR_start+i])

    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    fig.savefig(f"./result/{file_directory}/{file_name}.png", bbox_inches="tight")
    #plt.show()
    fig.clf()


    # X座標の列名
    x_cols = [f" X_{i}" for i in range(68)]
    # Y座標の列名
    y_cols = [f" Y_{i}" for i in range(68)]

    frame_num = 50
    landmarks_x = df.loc[frame_num, x_cols]
    landmarks_y = df.loc[frame_num, y_cols]
    
    x_cols_pixel = [f" x_{i}" for i in range(68)]
    y_cols_pixel = [f" y_{i}" for i in range(68)]
    landmarks_x_pixel = df.loc[frame_num, x_cols_pixel]
    landmarks_y_pixel = df.loc[frame_num, y_cols_pixel]
    
    width_max = max(landmarks_x_pixel)
    width_min = min(landmarks_x_pixel)
    height_max = max(landmarks_y_pixel)
    height_min = min(landmarks_y_pixel)

    for i in range(len(landmarks_x)) :
        plt.scatter(landmarks_x[i], landmarks_y[i])
        plt.text(landmarks_x[i], landmarks_y[i], f"{i}")
    
    face_size = np.sqrt((width_max-width_min)**2 + (height_max-height_min) **2)
            
    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.title(f"{file_name} landmark mapping({face_size:.2f})")
    plt.savefig(f"./result/{file_directory}/{file_name}_landmarkmapping.png", bbox_inches="tight")
    #plt.show()
    plt.clf()

    plt.plot(df.loc[:, " timestamp"], df.loc[:, " success"])
    plt.ylim(-0.1, 1.1)
    plt.title(f"{file_name} success rate(mean: {(count_success/num_of_row*100):.2f}%)")
    plt.savefig(f"./result/{file_directory}/{file_name}_success_rate.png", bbox_inches="tight")
    #plt.show()
    plt.clf()
    
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
    
    plt.plot(df.loc[:, " timestamp"], df.loc[:, " confidence"], label="confidence")
    plt.bar(df.loc[:, " timestamp"], df.loc[:, " success"], label="success_rate", linewidth=0, color="#ffc0c0", width=0.035)
    plt.legend()
    plt.ylim(-0.1, 1.1)
    plt.title(f"{file_name} landmark-estimation confidence(max_length:{confidence_length_max}/{len(confidence_list)})")
    plt.savefig(f"./result/{file_directory}/{file_name}_landmark_confidence.png", bbox_inches="tight")
    #plt.show()
    plt.clf()
    
for i in files :
        getAU(i)