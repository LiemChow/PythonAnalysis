# -*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup

filename = '../data/titles.txt'
html = urlopen("http://paper.people.com.cn/rmzk/html/2020-06/24/node_2651.htm")
bsObj = BeautifulSoup(html.read(), 'html.parser')
allText = bsObj.findAll({"li"}) and bsObj.findAll({"a"})
# print(allText)


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if (uchar >= u'\u4e00' and uchar <= u'\u9fa5') or uchar == u'\u000A':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if (uchar >= u'\u0030' and uchar <= u'\u0039'):
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def format_str(content):
    #content = unicode(content, 'utf-8')
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str + i
    return content_str


basic_str = str(allText)
basic_str = format_str(basic_str)
# print(basic_str)

with open(filename, 'w') as file_object:
    file_object.write(basic_str)

# 需要删除文本的第一行和最后一行
# 按行读入，删除最后一行和第一行
file_old = open('../data/titles.txt', 'r', encoding="utf-8")
lines = [i for i in file_old]
del lines[0]
del lines[-1]
file_old.close()
# 再覆盖写入
file_new = open('../data/titles.txt', 'w', encoding="utf-8")
file_new .write(''.join(lines))
file_new .close()
