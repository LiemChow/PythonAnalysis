# PythonAnalysis 项目介绍

[toc]



> 大三选修课信息内容安全的期末课程设计
>
> 这里我主要用Python对人民日报当日的新闻进行采集和分析

## 项目要求
1. 利用网络爬虫技术实现对某网站内容的采集
2. 采集下来的数据进行分词、预处理以及向量化表示
3. 进行简单的分析，如聚类，继承几个话题或者是情感倾向性分析，了解网民意见等等
4. 简单的可视化界面展示结果
5. 对分析的结果进行阐述

## 思路

* 使用`PyQt5`进行界面的设计

  `pip3 install pyqt5`

* 使用`JieBa`分词进行分词

  `pip3 install Jieba`

* 使用`matplotlib`来进行数据的数据可视化

  `pip3 install matplotlib`

* 

## 进度

* 点击退出按钮退出当前程序

  ![截屏2020-07-05 下午8.42.15](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-05 下午8.42.15.png)

* 点击日历图标显示当前日历

  ![截屏2020-07-05 下午8.39.31](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-05 下午8.39.31.png)
  
* 获取文章标题，打开人民日报，可以看到所有的文章标题都在`<li>`的标签内，所以用`BeautifulSoup`中的`findAll()`函数获取所有标题

  ![截屏2020-07-06 下午8.36.24](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-06 下午8.36.24.png)

* 
