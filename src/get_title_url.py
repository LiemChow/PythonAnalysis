from urllib.request import urlopen
from bs4 import BeautifulSoup

filename = '../data/titles_url.txt'
html = urlopen("http://paper.people.com.cn/rmzk/html/2020-06/24/node_2651.htm")
bsObj = BeautifulSoup(html.read(), 'html.parser')
#allText =bsObj.findAll("a", {"href": True}, {"target": "_blank"})
allText = bsObj.findAll("ul", {"id": True})

# print(allText)
with open(filename, 'w') as file_object:
    file_object.write(str(allText))


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
