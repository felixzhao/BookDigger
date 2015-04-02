#encoding:UTF-8
import requests
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

_start_page_url = 'http://book.douban.com/subject_search?start=15&search_text=%E5%91%BC%E5%85%B0%E6%B2%B3%E4%BC%A0&cat=1001'


def main_proc():
	print('Start get book list!')

	fout = open('../呼兰河传书目.txt','w')

	url_path = _start_page_url

	while True:
		print(url_path + ' ' + 'datetime? : ' + str(datetime.datetime.now()))
		try:
			print('开始新的一页处理。')

			response = requests.get(url_path)

			if response.status_code != 200:
				print("\n!!! 网络访问返回异常，异常代码：" + str(response.status_code) + " !!!\n")

			print('获取内容信息完成。')

			soup = BeautifulSoup(response.text)
			infos = soup.findAll('div',{'class':'info'})
			for info in infos:
				book_url = ''

				rating = ''
				pub = ''
				pl = ''

				rating_item = info.find('span',{'class':'rating_nums'})
				bookName = info.find('h2').a.attrs['title'].replace('\n','')

				info_a = info.find('a', href=True)
				book_url = info_a['href']

				pub_item = info.find('div',{'class':'pub'})
				pl_item = info.find('span',{'class':'pl'}).string

				if rating_item != None:
					rating = str(rating_item.string.replace('\n',''))
				if pub_item != None:
					pub = pub_item.string.replace('\n','')
				if pl_item != None:
					m = re.search('\d+', pl_item)
					if m != None:
						pl = m.group(0)

				#print(bookName + ' : ' + rating + ' ; ratingCount : ' + pl)
				print("### match : " + bookName + ' , ' + book_url + ' , ' + str(rating) + ' , ' +  pl + ' , \'' + pub.strip() + '\'')
				fout.write(bookName + ', \'' + book_url +'\' , ' + str(rating) + ' , ' +  pl + ' , \'' + pub.strip() + '\'')
				fout.write('\n')
			#fout.write("====== page " + str(int(i/20)) + ' ' + str(datetime.datetime.now()) + " ====== \n")
			#print("====== page " + str(int(i/20)) + ' ' + str(datetime.datetime.now()) + " ====== \n")

			# check next existed
			url_path = getNextPageUrl(soup)

			if url_path == '':
				break


			time.sleep(2)
		except Exception:
			print('get Exception.')
			print(sys.exc_info())
			pass
	fout.close()
	time.sleep(10)
	pass

	return

def getPageNumber ( para ):
	if para is None:
		return 0

	t = para.split('=')
	if len(t) < 2: 
		print('无页码.')
		return 0
	tt = t[1]
	t2 = tt.split('&')
	number = t2[0]

	if number.isdigit() == True:
		return int(number)
	else:
		return 0

def haveNextPage( spanContent):
	result = 0

	if spanContent is None:
		return 0

	next_a = spanContent.find('a', href=True)
	if next_a is None:
		return 0

	_href = next_a['href']
	print('\n下一页信息：' + _href + '\n')

	if _href is None:
		return 0

	page_num = getPageNumber(_href)			

	return page_num

def getNextPageUrl(soup):
	url = ''
	next = soup.find('span', {'class':'next'})
	if next is None:
		print('\n ！！！页面内容异常： 下一页 按钮不存在 ！！！ \n')
		return url
	cur_link = next.find('link')
	if cur_link is None: # 下一页不存在
		print('\n\n>>> 处理完成.\n')
	else:
		url = 'http://book.douban.com' + cur_link['href']
		page_num = getPageNumber(cur_link['href'])				
		print('\n >> 第 ' + str(page_num/15) + ' 页处理完成。\n')
	return url

#fcat = open('./catlogos_all.txt','r')

#name_list = fcat.readline().split()

#for name in name_list:
#	print('\n\n>>> ' + name + ' 开始处理.\n')
#	fout = open('./rating_out/' + name + '.txt','w')

	#flog = open('../page_content.race','w')

#	url_name = str(name.encode('UTF-8'))[2:-1].replace('\\x','%').upper()
#	url_root = "http://book.douban.com/tag/" + url_name
#	url_path = url_root

if __name__ == '__main__':
	print('hello world!')
	main_proc()
