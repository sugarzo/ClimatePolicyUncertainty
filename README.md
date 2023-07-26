# ClimatePolicyUncertainty  
参考[Gavriilidis(2021)](https://github.com/HaoningChen/ClimatePolicyUncertainty/blob/main/ref/Measuring%20Climate%20Policy%20Uncertainty.pdf)构建美国气候政策不确定性(CPU)指数的方法, 选取了人民日报、光明日报、中国青年报、浙江日报和经济日报构建中国的CPU

## 导航  
### 代码和demo:  
[code](https://github.com/HaoningChen/ClimatePolicyUncertainty/tree/main/code)  
### 参考文献和构建方法:  
[ref](https://github.com/HaoningChen/ClimatePolicyUncertainty/tree/main/ref)  

## 配置: 
Python3 + [requiresments.txt](https://github.com/HaoningChen/ClimatePolicyUncertainty/blob/main/requirements.txt) (Windows和Linux均可)

## 额外的发现  
由于众所周知的原因, 中国的新闻含p量十分高。因此似乎有必要弄清楚c, p和u的占比结构, 以及它们各自对cpu新闻在总新闻中占比的边际贡献。[supplemental_material](https://github.com/HaoningChen/ClimatePolicyUncertainty/blob/main/supplemental_material.csv)计算了人民日报, 光明日报, 经济日报和中国青年报各自的c, p, u, cp, cu, pu和cpu新闻在总新闻中的比例
