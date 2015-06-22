#encoding:UTF-8
import requests
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

import codecs

def getSoup(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text)
	return soup

def getPageCount(url):
	count = 0
	soup = getSoup(url)
	total = soup.find('span',{'id':'total-comments'})
	if total is not None:
		count = int(int(total.string[4:-2])/20)
	return count

def checkNext(cur, total):
	if cur < total:
		return True
	else:
		return False
	
def getComments(url):
	fout = codecs.open('Comments.txt','w',encoding='UTF-8')

	print(' ### Start Get Comments. ### ')
	url_path = url + 'comments/hot?p='

	page_num = 1
	try:
		page_count = getPageCount(url_path + str(page_num))
		if page_count is None or page_count == 0:
			print('No data need to dig.')
			return
		else:
			print(' !!! total page : ' + str(page_count))
		while True:
			print(' >>> Start Page : ' + str(page_num))
			url = url_path + str(page_num)

			soup = getSoup(url)
			infos = soup.findAll('li',{'class':'comment-item'})
			if infos is not None and len(infos) > 0:
				for info in infos:
					comment = info.find('p',{'class':'comment-content'})
					if comment is not None:
						content = comment.string
						print(' >>> ' + content)
						fout.write(content + '\n')
						fout.write

			if checkNext(page_num, page_count) == True:
				page_num += 1
				print(' >>> Page Done : ' + str(page_num))
			else:
				fout.close()
				print(" ### Get Comments Done at page : " + str(page_num) + " Total : " + str(page_count) + " ### ")
				return
			time.sleep(1)
			pass
	except Exception:
			print('get Exception.')
			print(sys.exc_info())
			pass
	

if __name__ == '__main__':
	url = 'http://book.douban.com/subject/1013380/'
	getComments(url)
