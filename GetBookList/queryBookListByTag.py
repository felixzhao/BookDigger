#encoding:UTF-8
import requests
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

def getInfo(soup):
    print('in get info.')
    result = ''
    a = soup.findAll('dl')
    for b in a:
        c = b.find('a',{'class':'title'})
        d = c.string
        print(d)
        result += d + '\n'
    return result

def getPage(url_path):
    print(url_path + ' ' + 'datetime? : ' + str(datetime.datetime.now()))
    try:
        print('开始新的一页处理。')

        response = requests.get(url_path)

        if response.status_code != 200:
            print("\n!!! 网络访问返回异常，异常代码：" + str(response.status_code) + " !!!\n")

        print('获取内容信息完成。')

        return response.text
        #soup = BeautifulSoup(response.text)

        time.sleep(1)
    except Exception:
        print('get Exception.')
        print(sys.exc_info())
        pass

def getList(url_path, fout):
        url_path += '?start='
        for i in range(0,100):
            p = url_path + str(i * 15)
            responseText = getPage(p)
            soup = BeautifulSoup(responseText)
            r = getInfo(soup)
            print(r)
            fout.write(r)
            fout.write('\n')
            fout.write(' >>>>>> the ' + str(i) + ' page. <<<<<<\n')
            fout.write('\n')

if __name__ == '__main__':
    name = '关于儿童文学的书'
    root = 'http://www.douban.com/tag/%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6/book'
    fout = open('../rating_out/' + name + '.txt','w')
    getList(root, fout)
    fout.close()
