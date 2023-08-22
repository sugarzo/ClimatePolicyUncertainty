import os
from datetime import datetime, timedelta
from time import sleep

import pywebio
from pywebio import pin
from pywebio.input import NUMBER, DATE
from pywebio.output import put_buttons, put_table, put_markdown, put_button, put_text, put_scope, clear

from ClimatePolicyUncertainty.webio.api import open_result_folder, open_code_folder, get_date_ranges, \
    NEWS_FOLDER, CPU_IDX_FOLDER, run_get_news, run_cpu, csv_to_list, FINAL_RESULT_FOLDER

data_to_name = {
    "gmrb.csv": "光明日报",
    "rmrb.csv": "人民日报",
    "jjrb.csv": "经济日报",
    "zjrb.csv": "浙江日报",
    "zqb.csv": "中国青年报"
}
yesterday = datetime.now() - timedelta(days=1)

event_loop = []  # type:[callable]


def ui_init():
    clear()
    pywebio.config(title='气候新闻 webui')
    put_markdown('# 气候新闻 webui')

    put_text(f"项目路径： {os.path.abspath('../')}")
    put_text(f"新闻数据路径： {os.path.abspath(NEWS_FOLDER)}")
    put_text(f"cpu_idx指数路径： {os.path.abspath(CPU_IDX_FOLDER)}")

    put_buttons(['打开项目文件夹', '刷新页面'], onclick=[lambda: open_code_folder(), lambda: {ui_init()}])

    put_markdown('## 当前数据集')
    put_buttons(['打开数据文件夹'], onclick=[lambda: open_result_folder()])

    new_data_list = get_date_ranges()
    data_table = []
    for new_data in new_data_list:  # type:tuple
        data_table.append([new_data[0], data_to_name.get(new_data[0], ""), new_data[1], new_data[2]]
                          + [put_button('查看', lambda: os.startfile(new_data[3]))])

    put_table(data_table, header=['数据集名字', '新闻来源', '开始时间', '结束时间', '操作'])

    put_markdown('**更新新闻数据集**')
    choices = []
    for data_name, news_name in data_to_name.items():
        choices.append(f"{news_name} {data_name}")
    put_table([[pin.put_checkbox("news_list", choices, value=choices),
                put_scope("table_1_scope", [
                    pin.put_input("input_date_start", label="开始日期", value="2023-05-01"),
                    pin.put_input("input_date_end", label="结束日期",
                                  value=yesterday.strftime("%Y-%m-%d"))]),
                put_scope("table_2_scope", [
                    pin.put_input("input_thread", label="并行数", type=NUMBER, value="4"),
                    pin.put_checkbox("input_merge", ["合并旧数据"], inline=True, value=["合并旧数据"]),
                    put_button('执行！',
                               onclick=lambda: event_loop.append(
                                   lambda: run_get_news(pin.pin["input_date_start"], pin.pin["input_date_end"],
                                                        [choose.split(' ')[1].split('.')[0] for choose in
                                                         pin.pin["news_list"]],
                                                        len(pin.pin["input_merge"]) > 0, pin.pin['input_thread']))),
                ])]
               ])
    put_markdown('## 计算指数')

    put_table([[put_scope("cpu_run_scope_1", [
        pin.put_input("input_cpu_date_start", label="开始日期", value="2023-05-01"),
        pin.put_input("input_cpu_date_end", label="结束日期", value=yesterday.strftime("%Y-%m-%d"))]),
                put_scope("cpu_run_scope_2", [
                    pin.put_checkbox("input_cpu_merge", ["合并旧数据"], inline=True, value=["合并旧数据"]),
                    put_button('开始计算',
                               onclick=lambda: run_cpu(pin.pin["input_cpu_date_start"], pin.pin["input_cpu_date_end"],
                                                       [choose.split(' ')[0] for choose in pin.pin["news_list"]],
                                                       len(pin.pin["input_cpu_merge"]) > 0))]
                          )]
               ]
              )

    put_markdown('### 历史cpu数据')
    put_table(csv_to_list(FINAL_RESULT_FOLDER + "idx.csv"))


if __name__ == '__main__':
    ui_init()
    while True:
        if len(event_loop) > 0:
            print("执行")
            for event in event_loop:
                event()
            event_loop = []
