from urllib.request import urlopen
from bs4 import BeautifulSoup

filename = '../data/titles.txt'
html = urlopen("http://paper.people.com.cn/rmzk/html/2020-06/24/node_2651.htm")
bsObj = BeautifulSoup(html.read(), 'html.parser')
allText = bsObj.findAll({"li"})
print(allText)

with open(filename,'w') as file_object:
    file_object.write(str(allText))

