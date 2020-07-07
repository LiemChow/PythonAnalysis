from urllib.request import urlopen
from bs4 import BeautifulSoup


# 根据得到的所有文章链接获取所有的文章内容
filename = '../data/pages.txt'

filelink = open('../data/titles_url.txt', 'r', encoding="utf-8")
linklines = [i for i in filelink]
filelink.close()


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
