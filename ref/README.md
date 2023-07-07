## 构建方法
参考:  [Measuring Climate Policy Uncertainty](https://github.com/HaoningChen/ClimatePolicyUncertainty/blob/main/ref/Measuring%20Climate%20Policy%20Uncertainty.pdf)  
### 方法具体如下(如果数学符号无法正常显示可以多刷新几次):  
(1) 按照频率 $freq$ , 对每家报纸 $j$ , 计算对应时间 $i$ 内的 $\frac{符合条件的新闻数}{频率内的新闻总数}$ , 记为 $s_{ij}$  
(2) 将 $s_{ij}$ 除以其在截面上的标准差 $sigma_{s_i}$, 将结果记为 $z_{ij}$, 并在截面上取 $z_{ij}$ 的均值 $m_i$  
(3) 对于时序数据 $m_i$, 将其除以自身的均值, 再乘100使最终结果的均值为100.  

## 语料库
参考:  [The dynamic spillover effects of climate policy uncertainty and coal price on carbon price: Evidence from China ](https://github.com/HaoningChen/ClimatePolicyUncertainty/blob/main/ref/The%20dynamic%20spillover%20effects%20of%20climate%20policy%20uncertainty%20and%20coal%20price%20on%20carbon%20price-Evidence%20from%20China.pdf)及其[附件](https://github.com/HaoningChen/ClimatePolicyUncertainty/blob/main/ref/The%20dynamic%20spillover%20effects%20of%20climate%20policy%20uncertainty%20and%20coal%20price%20on%20carbon%20price-Evidence%20from%20China-%E9%99%84%E5%BD%95.docx)

## 关于cpu的其它资料:  
[Climate Policy Uncertainty Index](http://www.policyuncertainty.com/climate_uncertainty.html)  
