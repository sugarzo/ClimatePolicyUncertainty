import os
from get_news_data import get_all_news
from process_news_data import pipeline, to_idx
import pandas as pd

# --- 可配置数据 ---
OUTPUT_FOLDER = "../result/"
NEWS_FOLDER = "../result/news_finished/"
CPU_IDX_FOLDER = "../result/cpu_idx/"
FINAL_RESULT_FOLDER = "../result/final_result/"

start_time = "2023-7-01"
end_time = "2023-07-15"
concat_old_data = True  # idx_csv是否尝试和原来的数据合并
get_new_data = False  # 是否爬取新的数据

# news_list = ["rmrb", "gmrb", "jjrb", "zjrb", "zqb"] # 可选择数据集
news_list = ["gmrb"]

# --- END 可配置数据 ----

def main():
    folders = [OUTPUT_FOLDER, NEWS_FOLDER, CPU_IDX_FOLDER, FINAL_RESULT_FOLDER]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    if get_new_data:
        result_dict = get_all_news(start_time, end_time, news_list)
        for news_title, news_result in result_dict.items():
            csv_file = os.path.join(NEWS_FOLDER, f"{news_title}.csv")
            combined_data = news_result
            # 检查原文件是否存在
            if os.path.isfile(csv_file):
                # 如果存在，读入旧的数据
                old_data = pd.read_csv(csv_file)
                # 合并旧的和新的数据
                combined_data = pd.concat([old_data, news_result])
                # 删除重复的行
                combined_data.drop_duplicates(inplace=True)
            combined_data.to_csv(csv_file, index=False, encoding="utf-8-sig")
    for news in news_list:
        if concat_old_data:
            score = pipeline(os.path.join(NEWS_FOLDER, f"{news}.csv", ), os.path.join(CPU_IDX_FOLDER, f"{news}.csv")
                             , name=news, save_mid_result=True, start=start_time, end=end_time)
        else:
            score = pipeline(os.path.join(NEWS_FOLDER, f"{news}.csv", ), name=news, save_mid_result=True,
                             start=start_time, end=end_time)
        score.to_csv(os.path.join(CPU_IDX_FOLDER, f"{news}.csv"))  # Save the ratio calculation result
    res = to_idx(CPU_IDX_FOLDER,OUTPUT_FOLDER, save_result=True)
    res.to_csv(os.path.join(FINAL_RESULT_FOLDER, "idx.csv"))


if __name__ == '__main__':
    main()
