import pandas as pd
import os

climate = ["气候", "气候变化", "二氧化碳", "低碳", "碳排放", "温室气体", "排放", "碳交易", "全球变暖", "绿色能源",
           "可再生能源", "环境", "新能源"]

policy = ["政策", "制度", "体制", "战略", "措施", "规章", "规例", "条例", "政治", "执政", "政府", "政委", "国务院",
          "人大", "人民代表大会", "中央", "国家主席", "总书记", "国家领导人", "总理", "改革", "整改", "整治", "规管",
          "监管", "环境保护税", "环保税", "人民银行", "央行", "碳中和", "碳达峰", "可持续", "可持续性"]

uncertainty = ["不确定", "不明确", "波动", "震荡", "动荡", "不稳", "未明", "不明朗", "不清晰", "未清晰", "难料",
               "难以预料", "难以预测", "难以预计", "难以估计", "无法预料", "无法预测", "无法预计", "无法估计",
               "不可预料", "不可预测", "不可预计", "不可估计"]


def process_datetime(df: pd.DataFrame, start: str = "2010-12-01", end: str = "2023-06-30",
                     freq: str = "month") -> pd.DataFrame:
    """
    :param df: news dataset
    :param start: the exact date you want to start with
    :param end: the exact date you want to end your analysis
    :param freq: "datetime", "month" or "year"
    :return:
    """
    df["datetime"] = pd.to_datetime(df["datetime"])
    if freq == "month":
        df["month"] = df["datetime"].dt.strftime("%Y-%m")  # 注意这里保留了年份
    elif freq == "year":
        df["year"] = df["datetime"].dt.strftime("%Y")
    df = df[df["datetime"] >= pd.to_datetime(start)]
    df = df[df["datetime"] <= pd.to_datetime(end)]
    if freq != "datetime":
        df.set_index([freq, "datetime"], inplace=True)
    else:
        df.set_index(["datetime"], inplace=True)
    df.fillna("nan", inplace=True)  # 将缺失值填充为字符串 'nan'
    print(df.info())
    print(df.head(1))
    return df


def check_isin_cpu(data: pd.DataFrame, c: list = None, p: list = None, u: list = None,
                   show_detail=False) -> pd.DataFrame:
    if c is None:
        c = climate
    if p is None:
        p = policy
    if u is None:
        u = uncertainty

    isin_c: list[int] = [0 for _ in range(len(data))]
    isin_p: list[int] = [0 for _ in range(len(data))]
    isin_u: list[int] = [0 for _ in range(len(data))]
    isin_cpu: list[int] = [0 for _ in range(len(data))]

    for i in range(len(data)):
        for c_word in c:
            if c_word in data["title"][i] or c_word in data["article"][i]:
                isin_c[i] = 1
                break
        for p_word in p:
            if p_word in data["title"][i] or p_word in data["article"][i]:
                isin_p[i] = 1
                break
        for u_word in u:
            if u_word in data["title"][i] or u_word in data["article"][i]:
                isin_u[i] = 1
                break
    for i in range(len(data)):
        if isin_c[i] == 1 and isin_p[i] == 1 and isin_u[i] == 1:  # 注意这里需要的是与还是或的关系
            isin_cpu[i] = 1
    data["isin_cpu"] = isin_cpu

    # 接下来考虑c, p, u各部分的特征及对cpu新闻占比的边际贡献。由于研究的主要目的不在于此, 故计算结果比较粗略
    # 考虑到中国最近的新闻可能含p量较高, 因此似乎有必要查看p对cpu新闻占比的边际贡献。
    if show_detail:
        num_c, num_p, num_u = 0, 0, 0
        num_cu, num_pu, num_cp, num_cpu = 0, 0, 0, 0
        for i in range(len(isin_c)):
            if isin_c[i] == 1:
                num_c += 1
            if isin_p[i] == 1:
                num_p += 1
                if isin_c[i] == 1:
                    num_cp += 1
            if isin_u[i] == 1:
                num_u += 1
                if isin_c[i] == 1:
                    num_cu += 1
                if isin_p[i] == 1:
                    num_pu += 1
            if isin_cpu[i] == 1:
                num_cpu += 1
        print("%c: ", num_c / len(isin_c))
        print("%p: ", num_p / len(isin_p))
        print("%u: ", num_u / len(isin_u))
        print("%c&p: ", num_cp / len(isin_c))
        print("%c&u: ", num_cu / len(isin_c))
        print("%p&u: ", num_pu / len(isin_c))
        print("%c&p&u: ", num_cpu / len(isin_c), '\n')
    return data


def norm_news_data_by_freq(data: pd.DataFrame, target: str = "isin_cpu", freq: str = "month",
                           name: str = "score", save_mid_result: bool = False) -> pd.Series:
    """
    按照给定的频率将对应频率内的新闻数量放缩至[0, 1]区间

    :param data:
    :param target:
    :param freq:
    :param name:
    :param save_mid_result: 是否保存中间结果
    :return:
    """
    total_news_mth = data[target].groupby(freq).count()
    num_news_selected = data[target].groupby(freq).apply(lambda x: x[x.values == 1].count())
    norm = pd.Series(num_news_selected.values / total_news_mth.values, index=num_news_selected.index, name=name)
    if save_mid_result:
        result = pd.DataFrame({"news_selected": num_news_selected, "total_news": total_news_mth, "ratio": norm})
        result.to_csv(name + ".csv")
    return norm


def pipeline(filepath: str, encoding: str = "utf-8-sig", start: str = "2010-12-01", end: str = "2023-06-30",
             multiplier: int = 1, name: str = "score", freq: str = "month", save_mid_result: bool = False,
             show_cpu_detail=False) -> pd.Series:
    """
    example:
    folder_path = "D:/Desktop/news_finished/"
    target_dir = "D:/Desktop/cpu_idx/"

    score = pipeline(folder_path + "gmrb.csv", name="gmrb")
    score.to_csv(target_dir + "gmrb.csv")

    :param filepath: 数据文件的地址
    :param encoding: 编码格式, 默认utf-8-sig
    :param start: 起始时间
    :param end: 结束时间
    :param multiplier: 乘数(考虑经济意义)
    :param name: 输出的Series的名字
    :param freq: 计算cpu所按的时间频率
    :param save_mid_result: 是否保存中间结果(每月符合条件的新闻数和每月新闻总数)
    :param show_cpu_detail: 是否输出更详细的cpu统计结果
    :return:
    """
    data = pd.read_csv(filepath, encoding=encoding)
    data = process_datetime(data, start=start, end=end, freq=freq)
    data = check_isin_cpu(data, show_detail=show_cpu_detail)
    score = norm_news_data_by_freq(data, name=name, freq=freq, save_mid_result=save_mid_result)
    score *= multiplier
    return score


def to_idx(folder_path: str, multiplier: int = 100, freq: str = "month", save_result: bool = False) -> pd.Series:
    """
    参考这段话:
    For each newspaper, he scales the number of relevant articles per month with the total number of
    articles during the same month.
    Next, these eight series are standardized to have a unit standard deviation and then averaged across
    newspapers by month.
    Finally, the averaged series are normalized to have a mean value of 100 for the period 2000:M1-2021:M3.

    具体而言:
    (1) 按照频率freq, 对每家报纸j, 计算对应时间i内的 符合条件的新闻数 / 频率内的新闻总数, 记为 s_ij(已经在pipeline函数中计算)
    (2) 将 s_ij 除以其在截面上的标准差 sigma_si, 将结果记为 z_ij, 并在截面上取 z_ij 的均值 m_i
    (3) 对于时序数据 m_i, 将其除以自身的均值, 再乘上一个乘数(默认为100)得到最终结果

    :param folder_path: 文件夹地址, 程序会读入该文件夹下面所有csv文件, 并按照上述步骤计算指数
    :param multiplier: 乘数, 默认为100
    :param freq: "month"按月, "datetime"按天, 其它频率可自定义
    :param save_result: 是否保存 z_ij 的均值 m_i
    :return:
    """

    def process_single_idx(data: pd.DataFrame) -> pd.DataFrame:
        # data.set_index("month", inplace=True)
        newspaper_name = data.columns[1]
        data.columns = [freq, "score"]
        data["name"] = newspaper_name
        return data

    def cummean(data: pd.Series) -> pd.Series:
        cumsum = data.cumsum()
        count = [i + 1 for i in range(len(data))]
        cmean = []
        for i in range(len(cumsum)):
            res = cumsum.values[i] / count[i]
            cmean.append(res[0])
        return pd.Series(cmean, index=data.index, name="score")

    all_idx = pd.DataFrame()
    files = os.listdir(folder_path)
    for file in files:
        target = folder_path + file
        df = pd.read_csv(target)
        df = process_single_idx(df)
        all_idx = pd.concat([all_idx, df], axis=0)
    # all_idx[freq] = pd.to_datetime(all_idx[freq])
    all_idx = all_idx.set_index([freq, "name"]).sort_index()
    # std = all_idx.groupby(freq).std()
    std = all_idx.groupby("name").std()
    all_idx /= std
    mean_zscore = all_idx.groupby(freq).mean()
    scaled_zscore = mean_zscore / mean_zscore.mean()  # 如果要将结果的均值控制在100, 就必须用所有样本计算均值

    if save_result:
        cummean = cummean(mean_zscore)
        # 原文中是用所有样本的均值, 但这样有未来函数. 此处可考虑改为用历史样本(从t0开始到当下时间段的均值, 即m_i序列)
        # scaled_zscore = pd.Series(mean_zscore.values.flatten() / cummean.values, index=cummean.index)
        result = cummean
        result.to_csv("mu.csv")
    scaled_zscore *= multiplier
    scaled_zscore.name = "score"
    print(scaled_zscore)
    return scaled_zscore
