# python3 输出中文对象到json格式的文件
from __future__ import unicode_literals
import json
import urllib3
import urllib
from bs4 import BeautifulSoup
import re
import sys

def getElString(el):
    temp = ""
    for string in el.stripped_strings:
        temp += repr(string).strip("'").replace("\\xa0"," ")
    return temp

def getNews(url):
	http = urllib3.PoolManager()
	r = http.request('GET', url)
	news = []
	if r.status==200:
	    soup = BeautifulSoup(r.data, "lxml")
	    divs = soup.find_all("div")

	    for div in divs:
	    	# print(getElString(div))
	    	item = {}
	    	if div["class"][0]=="vrwrap":
	            if div.h3==None:
	                break
	            item["href"] = div.h3.a["href"] #新闻链接
	            item["title"] = getElString(div.h3.a) #新闻标题
	            #新闻内展示图片
	            src = re.search("&url=(.*)[&]*",div.img["src"])
	            item["image"]=""
	            if src!=None:
	                item["image"] = urllib.parse.unquote(src.group(1))
	                if "htm" in item["image"].split(".")[-1]:
	                    item["image"] = ""
	            ps = div.find_all("p")
	            item["from_time"] = getElString(ps[0]) #新闻时间
	            if ps[1].span!=None:
	                item["summary"] = getElString(ps[1].span) #新闻摘要
	            else:
	                item["summary"] = getElString(ps[1]) #新闻摘要
	            news.append(item)
	return news

if __name__ == '__main__':
	url = 'http://news.sogou.com/news?query=%E7%94%B5%E5%BD%B1'
	news = getNews(url)
	fileName = "news.json"
	#若命令行指定fileName,则覆盖默认的值

	if len(sys.argv) > 1:
		fileName = sys.argv[1]
	with open(fileName, "w", encoding="utf-8") as f:
		json.dump(news, f, ensure_ascii=False)