* # 人民周刊信息采集分析论文报告

  

  

  

  ## 实验要求和设计

  ### 实验目的

  ​		课程论文的目的是检验大家对课程的学习状况，同时，根据指定的题目，查阅文献、动手实现，并加以分析整理形成课程论文。从而达到对学生文献查阅、编程实现、论文撰写的能力培养，同时加深学生对该专题问题的认识，提升本专题学习的效果。

  ### 实验要求

  1. 利用网络爬虫技术实现对某网站内容的采集
  2. 采集下来的数据进行分词、预处理以及向量化表示
  3. 进行简单的分析，如聚类，聚成几个话题或者是情感倾向性分析，了解网民的意见等等
  4. 简单的可视化界面展示结果
  5. 对分析的结果进行阐述

  ### 项目设计

  ​		这里我将设计一个Mac上的app，用来获取人民周刊上当前周的所有文章和标题，然后进行数据的统计分析。整个程序使用的是Python语言以及Python额外的库，故理论可以在任何已安装Python3及以上版本的平台运行，但只在Mac OS平台运行过，不知道在其他平台表现如何。		

  ### 设计思路功能

  1. 主界面可视化的界面，利用python3的pyqt5库进行界面设计
  2. 利用PyQt5中的Calculator日历模块来调取系统时间，获取日历
  3. 分析网页链接后，利用Python3的BeautifulSoup模块获取今日周刊一周内所有的文章和内容，并把标题整理显示出来
  4. 利用Python3的Jieba分词来对文章进行分词（全模式），然后用百度停用词表（该表主要针对新闻类文章）过滤掉停用词
  5. 利用Python3自带的collections模块来统计高频词汇，并通过`matplotlib`和`pygal`来绘制统计图表
  6. 利用`Python3`中的`sklearn`模块来计算TF-IDF来计算词语在向量中的权重
  7. 利用`sklearn.cluster`来进行`K-means`聚类

  ### 实验环境和其他配置

  #### 实验环境

  操作系统：macOS Catalina 10.15.5

  文本编辑器：Sublime Text

  编程语言：Python 3.8.3

  #### Python3扩展包配置

  ```shell
  pip3 install pyqt5
  pip3 install BeautifulSoup4
  pip3 install jieba
  pip3 install matplotlib
  pip3 install pygal
  pip3 install sklearn
  ```

  

  ## 代码实现以及过程

  ​		这里我将会采集人民日报当周的所有日报的数据进行分析。包括两个部分，一个是简单的数据预处理和统计，另一部分是数据聚类处理。

  ### 简单的数据预处理

  1. 获取日历模块，这里主要是调取系统的日历，查看对应当前周刊的日期。

     ```python
     ...
     import sys
     from PyQt5.QtWidgets import (QWidget, QCalendarWidget,
                                  QLabel, QApplication)
     from PyQt5.QtCore import QDate
     
     
     class Calculator(QWidget):
         def __init__(self):
             super().__init__()
     
             self.initUI()
     
         def initUI(self):
             cal = QCalendarWidget(self)
             cal.setGridVisible(True)
             cal.move(20, 20)
             cal.clicked[QDate].connect(self.showDate)
     
             self.lbl = QLabel(self)
             date = cal.selectedDate()
             self.lbl.setText(date.toString())
             self.lbl.move(130, 260)
     
             self.setGeometry(300, 300, 350, 300)
             self.setWindowTitle('Calendar')
             self.show()
     
         def showDate(self, date):
             self.lbl.setText(date.toString())
     ...
     ```

     ![截屏2020-07-07 下午5.44.42](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午5.44.42.png)

  2. 获取标题并且过滤，使用`BeautifulSoup4`库中的`findAll()`函数获取所有的文章标题链接。查看网页源码，可以看到标题都被`li`和`a`标记，故使用`bsObj.findAll({"li"}) and bsObj.findAll({"a"})`

     ![截屏2020-07-07 下午5.22.37](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午5.22.37.png)

     ```python
     ...
     # 得到所有的文章标题
     filename = '../data/titles.txt'
     html = urlopen("http://paper.people.com.cn/rmzk/html/2020-06/24/node_2651.htm")
     bsObj = BeautifulSoup(html.read(), 'html.parser')
     allText = bsObj.findAll({"li"}) and bsObj.findAll({"a"})
     ...
     
     # 文章标题，按行读入，删除最后一行和第一行
     file_old = open('../data/titles.txt', 'r', encoding="utf-8")
     lines = [i for i in file_old]
     del lines[0]
     del lines[-1]
     file_old.close()
     # 再覆盖写入
     file_new = open('../data/titles.txt', 'w', encoding="utf-8")
     file_new .write(''.join(lines))
     file_new .close()
     ```

     ![截屏2020-07-07 下午5.25.45](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午5.25.45.png)

     

  3. 获取所有文章的链接，再次分析网页的源码发现，文章的链接都有`id`标记，就同第二步所述，利用`bsObj.findAll("ul", {"id": True})`来获取文章的所有链接，注意这里是二级超链接，需要加上一级链接，会在获取文章时处理。

     ![截屏2020-07-07 下午5.27.29](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午5.27.29.png)

     ```python
     ...
     #获取每篇文章的链接
     filename = '../data/titles_url.txt'
     html = urlopen("http://paper.people.com.cn/rmzk/html/2020-06/24/node_2651.htm")
     bsObj = BeautifulSoup(html.read(), 'html.parser')
     #allText =bsObj.findAll("a", {"href": True}, {"target": "_blank"})
     allText = bsObj.findAll("ul", {"id": True})
     ...
     
     ...
     #简单处理一下获取的内容，删掉无用的标记
     # 获取链接
     file_old = open('../data/titles_url.txt', 'r', encoding="utf-8")
     lines = [i for i in file_old]
     # print(lines[22])
     for i in range(len(lines) - 1, -1, -1):
         if 'href' in lines[i] and 'htm' in lines[i]:
             continue
         else:
             lines.remove(lines[i])
     file_old.close()
     
     # 再覆盖写入
     file_new = open('../data/titles_url.txt', 'w', encoding="utf-8")
     file_new .write(''.join(lines))
     file_new .close()
     ...
     ```

     ![截屏2020-07-07 下午5.32.26](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午5.32.26.png)

  4. 获取所有文章的内容，这里通过第三步获取的文章链接，获取二级链接下文章的所有内容，简单去除非汉字后存储在`pages.txt`文件下。

     ```python
     ...
     # 根据得到的所有文章链接获取所有的文章内容
     filename = '../data/pages.txt'
     pagesfile = open('../data/pages.txt', 'w', encoding="utf-8")
     for i in range(len(linklines) - 1):
         urllink = "http://paper.people.com.cn/rmzk/html/2020-06/24/content_" + \
             str(1994733 + i) + ".htm"
         html = urlopen(urllink)
         bsObj = BeautifulSoup(html.read(), 'html.parser')
         allText = bsObj.findAll({"p"})
     
         basic_str = str(allText)
         basic_str = format_str(basic_str)
     
         pagesfile.write(''.join(str(basic_str)))
     
     
     pagesfile.close()
     ...
     ```

     ![截屏2020-07-07 下午5.43.23](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午5.43.23.png)

  5. 简单的文本预处理：使用`Jieba`对文章的内容进行分词，然后去除停用词，最后`collections`统计出出现次数最多的词，并通过`matplotlib``pygal`来输出最多前21个词汇以及次数的svg图像。停用词去除时，百度停用词对新闻支持比较好。（注：SVG图像需要借助浏览器或者有支持图形插件的软件打开，比如adobe Photoshop，affinity Photo，无法使用诸如未安装拓展的Microsoft exel等图表软件打开，这里我用的是MacBook pro自带的safari浏览器）

     ```python
     from collections import Counter
     import jieba
     
     # jieba.load_userdict('userdict.txt')
     # 创建停用词list
     
     
     def stopwordslist(filepath):
         stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
         return stopwords
     
     
     # 对句子进行分词
     def seg_sentence(sentence):
         sentence_seged = jieba.cut(sentence.strip())
         stopwords = stopwordslist('../data/百度停用词表.txt')  # 这里加载停用词的路径
         outstr = ''
         for word in sentence_seged:
             if word not in stopwords:
                 if word != '\t':
                     outstr += word
                     outstr += " "
         return outstr
     
     
     inputs = open('../data/pages.txt', 'r')  # 加载要处理的文件的路径
     outputs = open('../data/pages_deal_1.txt', 'w')  # 加载处理后的文件路径
     for line in inputs:
         line_seg = seg_sentence(line)  # 这里的返回值是字符串
         outputs.write(line_seg)
     outputs.close()
     inputs.close()
     # WordCount
     with open('../data/pages_deal_1.txt', 'r') as fr:  # 读入已经去除停用词的文件
         data = jieba.cut(fr.read())
     data = dict(Counter(data))
     
     # 排序
     data = sorted(data.items(), key=lambda item: item[1], reverse=True)
     
     with open('../data/wordcount.txt', 'w') as fw:  # 读入存储wordcount的文件路径
         for k, v in data:
             fw.write('%s,%d\n' % (k, v))
     
     with open('../data/wordfinal.txt', 'w') as fileobject:
         for k, v in data:
             fileobject.write(k + ' ')
     
     # 以图表的形式展现频率最高的50个词
     import pygal
     frequencies = []
     words = []
     
     i = 0
     for k, v in data:
         if i == 0:
             i += 1
             continue
         words.append(k)
         frequencies.append(v)
         i += 1
         if i >= 21:
             break
     
     
     hist = pygal.Bar()
     hist.title = "高频词汇统计"
     
     hist.x_labels = words
     hist.x_title = "高频词汇"
     
     hist.add('出现次数', frequencies)
     hist.render_to_file("../data/words_frequencies.svg")
     ```

     ![截屏2020-07-07 下午10.10.50](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午10.10.50.png)

     

  

  ### 文本的聚类分析

  1. 将之前的文章按照顺序保存在`..data/pages/`路径下。

     ![截屏2020-07-08 下午3.36.21](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午3.36.21.png)

  2. 同上的分词和文本预处理。这里改进了上述的不足，新增用户字典，避免有些词汇被删除。

     ![截屏2020-07-08 下午3.49.41](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午3.49.41.png)

  3. 将所有文章保存在一个文档`pages_result.txt`下，以便后面处理。

     ```python
     import re
     import os
     import sys
     import codecs
     import shutil
     
     
     def merge_file():
         path = "../data/pages/"
         resName = "../data/pages_result.txt"
         if os.path.exists(resName):
             os.remove(resName)
         result = codecs.open(resName, 'w', 'utf-8')
     
         num = 1
         while num <= 44:
             name = num
             fileName = path + str(name) + ".txt"
             source = open(fileName, 'r')
             line = source.readline()
             line = line.strip('\n')
             line = line.strip('\r')
     
             while line != "":
                 #line = unicode(line, "utf-8")
                 line = line.replace('\n', ' ')
                 line = line.replace('\r', ' ')
                 result.write(line + ' ')
                 line = source.readline()
             else:
                 print('End file: ' + str(num))
                 result.write('\r\n')
                 source.close()
             num = num + 1
     
         else:
             print('End All')
             result.close()
     
     
     if __name__ == '__main__':
         merge_file()
     ```

     ![截屏2020-07-08 下午3.59.06](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午3.59.06.png)

  4. 计算TF—IDF，这里需要导入包`sklearn`。它表示TF（词频）和IDF（倒文档频率）的乘积。

     ```python
     # coding=utf-8
     """
     Created on 2015-12-30 @author: Eastmount
     """
     
     import time
     import re
     import os
     import sys
     import codecs
     import shutil
     from sklearn.feature_extraction.text import TfidfTransformer
     from sklearn.feature_extraction.text import CountVectorizer
     
     '''
     sklearn里面的TF-IDF主要用到了两个函数：CountVectorizer()和TfidfTransformer()。
         CountVectorizer是通过fit_transform函数将文本中的词语转换为词频矩阵。
         矩阵元素weight[i][j] 表示j词在第i个文本下的词频，即各个词语出现的次数。
         通过get_feature_names()可看到所有文本的关键字，通过toarray()可看到词频矩阵的结果。
         TfidfTransformer也有个fit_transform函数，它的作用是计算tf-idf值。
     '''
     
     if __name__ == "__main__":
         corpus = []  # 文档预料 空格连接
     
         # 读取预料 一行预料为一个文档
         for line in open('../data/pages_result.txt', 'r').readlines():
             print(line)
             corpus.append(line.strip())
         # print corpus
         time.sleep(5)
     
         # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
         vectorizer = CountVectorizer()
     
         # 该类会统计每个词语的tf-idf权值
         transformer = TfidfTransformer()
     
         # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
         tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
     
         # 获取词袋模型中的所有词语
         word = vectorizer.get_feature_names()
     
         # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
         weight = tfidf.toarray()
     
         resName = "../data/pages_tf_result.txt"
         result = codecs.open(resName, 'w', 'utf-8')
         for j in range(len(word)):
             result.write(word[j] + ' ')
         result.write('\r\n\r\n')
     
         # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
         for i in range(len(weight)):
             print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
             for j in range(len(word)):
                 result.write(str(weight[i][j]) + ' ')
             result.write('\r\n\r\n')
     
         result.close()
     ```

  5. K-means聚类，这里主要是调用`sklearn.cluster`实现

     ```python
     ...
     print('Start Kmeans:')
         from sklearn.cluster import KMeans
         clf = KMeans(n_clusters=44)
         s = clf.fit(weight)
         print(s)
     
         # 44个中心点
         print(clf.cluster_centers_)
     
         # 每个样本所属的簇
         print(clf.labels_)
         i = 1
         while i <= len(clf.labels_):
             print(i, clf.labels_[i - 1])
             i = i + 1
     
         # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
         print(clf.inertia_)
     ...
     ```

     ![截屏2020-07-08 下午4.14.16](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午4.14.16.png)	![截屏2020-07-08 下午5.40.52](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午5.40.52.png)

     

     

     ## 程序运行结果

     ### 主界面

     pyqt设计主界面，对应的按钮分别为退出程序，显示日历，爬取信息，统计高频词汇、显示所有标题，词语聚类统计，如图，鼠标移动到对应按钮即显示功能提示。

  ![截屏2020-07-08 下午6.21.04](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午6.21.04.png)

  ### 日历按钮

  点击日历图表，即可显示调出日历，查看当前周信息。

  ![截屏2020-07-08 下午6.23.10](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午6.23.10.png)

  ### 获取今日文章

  点击分析按钮，获取所有信息后再点击文章按钮，获取标题。

  ![截屏2020-07-08 下午6.25.43](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午6.25.43.png)

  ### 统计高频词汇

  ![截屏2020-07-07 下午10.10.50](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-07 下午10.10.50-4203989.png)

  ### 文本聚类结果

  ![截屏2020-07-08 下午6.30.28](/Users/linqun/Documents/GitHub/PythonAnalysis/截屏2020-07-08 下午6.30.28.png)

  ## 数据分析

  1. 通过高词频数据统计结果可知，本周的高频词汇依旧为发展、疫情、经济、中国、工作、国家、建设、生态、社会、保护、生活等，这和今年的疫情和国际经济的发展离不开，也昭示着今年的国情。
  2. 通过对文本的聚类分析，每一类词汇都相互联系，例如组中的医用、医生、医治、医界、医疗等。

  ## 实验不足和总结

  1. 聚类的结果没有通过图表的形式展示出来，难以达到直观的效果
  2. 本次实验，在文本向量化中采用了最快速和比较了解的TF-IDF方法，没有考虑过one-hot等其他方法。
  3. k-means方法的缺陷。Kmeans聚类是一种自下而上的聚类方法，它的优点是简单、速度快；缺点是聚类结果与初始中心的选择有关系，且必须提供聚类的数目。Kmeans的第二个缺点是致命的，因为在有些时候，我们不知道样本集将要聚成多少个类别，这种时候kmeans是不适合的，推荐使用hierarchical 或meanshift来聚类。第一个缺点可以通过多次聚类取最佳结果来解决。
  4. 本次项目，挂载到了GitHub上，使用git的commit记录了每一次的代码修改。（https://github.com/lin-2333/PythonAnalysis）

  
