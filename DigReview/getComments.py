#encoding:UTF-8
import requests
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

def getPageCount(url):
	count = 0
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	print(soup)
	total = soup.find('span',{'id':'total-comments'})
	if total is not None:
		count = int(total.string[4:-2])
	return count

def checkNext(cur, total):
	if cur < total:
		return True
	else:
		return False

def main():
	fout = open('../Comments.txt','w')

	print(' ### Start Get Comments. ### ')
#	url_path = 'http://book.douban.com/subject/1060852/comments/hot?p='
	url_path = 'http://book.douban.com/subject/4843155/comments/hot?p='
	page_num = 1
	try:
		page_count = getPageCount(url_path + str(page_num))
		if page_count is None or page_count == 0:
			print('No data need to dig.')
			return
		else:
			print(' !!! total page : ' + str(page_count))
		while True:
			print('Start Page : ' + str(page_num))
			url = url_path + str(page_num)

			response = requests.get(url)
			soup = BeautifulSoup(response.text)
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
			else:
				fout.close()
				print(" ### Get Comments Done at page : " + str(page_num) + " ### ")
				return
			sleep(2)
			pass
	except Exception:
			print('get Exception.')
			print(sys.exc_info())
			pass
	

if __name__ == '__main__':
	main()
