# from get_news_data import get_gmrb_data
from process_news_data import pipeline, to_idx


folder = "D:/Desktop/news_finished/"  # 使用get_news_data模块获取新闻, 并将新闻文件(csv格式)放在folder文件夹下
# news = get_gmrb_data(start="2010-01-01", end="2023-06-30")  # 推荐逐年获取, 最后用get_news_data.merge_news_data()合并成一份
# news.to_csv(folder + "gmrb.csv", encoding="utf-8-sig")

news_list = ["rmrb", "gmrb", "jjrb", "zjrb", "zqb"]
for news in news_list:
    score = pipeline(folder + news + ".csv", name=news, save_result=True)
    score.to_csv("D:/Desktop/cpu_idx/" + news + ".csv")

res = to_idx("D:/Desktop/cpu_idx/", save_result=True)
res.to_csv("D:/Desktop/final_result/idx.csv")
