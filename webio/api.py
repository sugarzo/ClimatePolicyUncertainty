import csv
import os

import pandas as pd

from ClimatePolicyUncertainty.code.get_news_data import get_all_news
from ClimatePolicyUncertainty.code.process_news_data import pipeline, to_idx

# --- 可配置数据 ---
OUTPUT_FOLDER = "../result/"
NEWS_FOLDER = "../result/news_finished/"
CPU_IDX_FOLDER = "../result/cpu_idx/"
FINAL_RESULT_FOLDER = "../result/final_result/"

concat_old_data = True  # idx_csv是否尝试和原来的数据合并
get_new_data = False  # 是否爬取新的数据


def open_result_folder():
    os.startfile(r"..\result")


def open_code_folder():
    os.startfile(r"..\code")


def get_date_ranges():
    directory = NEWS_FOLDER
    date_ranges = []

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            # 读取第一行和最后一行
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                first_line = lines[1]
                # 从文件末尾开始，找到第一个非空行
                for i in range(-1, -len(lines), -1):
                    if 1 < len(lines[i].split(',')):
                        last_line = lines[i]
                        break
            # 使用pandas处理CSV
            first_date = first_line.split(',')[0]
            last_date = last_line.split(',')[0]
            date_ranges.append((filename, first_date, last_date, file_path.replace('/', '\\')))
    print(date_ranges)
    return date_ranges


def run_get_news(start_time, end_time, news_list, merge=False, n_jobs=-1):
    print(start_time, end_time, news_list, merge)
    result_dict = get_all_news(start_time, end_time, news_list)

    for news_title, news_result in result_dict.items():
        csv_file = os.path.join(NEWS_FOLDER, f"{news_title}.csv")
        combined_data = news_result
        if merge and os.path.isfile(csv_file):
            old_data = pd.read_csv(csv_file)
            combined_data = pd.concat([old_data, news_result])
            combined_data.drop_duplicates(inplace=True)
        combined_data.to_csv(csv_file, index=False, encoding="utf-8-sig")


def run_cpu(start_time, end_time, news_list, concat_old_data=True):
    for news in news_list:
        if concat_old_data:
            score = pipeline(os.path.join(NEWS_FOLDER, f"{news}.csv", ), os.path.join(CPU_IDX_FOLDER, f"{news}.csv")
                             , name=news, save_mid_result=True, start=start_time, end=end_time)
        else:
            score = pipeline(os.path.join(NEWS_FOLDER, f"{news}.csv", ), name=news, save_mid_result=True,
                             start=start_time, end=end_time)
        score.to_csv(os.path.join(CPU_IDX_FOLDER, f"{news}.csv"))
    res = to_idx(CPU_IDX_FOLDER, OUTPUT_FOLDER, save_result=True)
    res.to_csv(os.path.join(FINAL_RESULT_FOLDER, "idx.csv"))


def csv_to_list(csv_file_path):
    data_list = [[]]
    try:
        with open(csv_file_path.replace('/', '\\'), 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            data_list = list(reader)
    except:
        pass
    return data_list
