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

i = 0
with open('../data/wordfinal_100.txt', 'w') as fileobject:
    for k, v in data:
        fileobject.write(k + ' ')
        if i > 100:
            break
        i += 1
