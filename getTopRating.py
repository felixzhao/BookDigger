#encoding:UTF-8
import urllib.request
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

fcat = open('./catlogos_all.txt','r')

name_list = fcat.readline().split()

for name in name_list:
	fout = open('./rating_out/' + name + '.txt','w')
	for i in range(0,800,20):
		url_name = str(name.encode('UTF-8'))[2:-1].replace('\\x','%').upper()
		url_path = "http://book.douban.com/tag/" + url_name + "?start=" + str(i) +"&type=T"
		print(url_path)
		print('datetime? : ' + str(datetime.datetime.now()))
		try:
			print('==>start get page.')
			#req = urllib.Request(url_path, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
			page = urllib.request.urlopen(url_path)
			data = page.read()
			data = data.decode('UTF-8')

			soup = BeautifulSoup(data)
			infos = soup.findAll('div',{'class':'info'})
			for info in infos:
				rating = ''
				pub = ''
				pl = ''

				rating_item = info.find('span',{'class':'rating_nums'})
				bookName = info.find('h2').a.attrs['title'].replace('\n','')
				pub_item = info.find('div',{'class':'pub'})
				pl_item = info.find('span',{'class':'pl'}).string

				if rating_item != None:
					rating = rating_item.string.replace('\n','')
				if pub_item != None:
					pub = pub_item.string.replace('\n','')
				if pl_item != None:
					m = re.search('\d+', pl_item)
					pl = m.group(0)

				#print(bookName + ' : ' + rating + ' ; ratingCount : ' + pl)

				if rating.startswith('9') and int(pl) > 3000:
					print("### match : " + bookName + ' , ' + rating + ' , ' +  pl + ' , \'' + pub.strip() + '\'')
					fout.write(bookName + ' , ' + rating + ' , ' +  pl + ' , \'' + pub.strip() + '\'')
					fout.write('\n')
			#fout.write("====== page " + str(int(i/20)) + ' ' + str(datetime.datetime.now()) + " ====== \n")
			print("====== page " + str(int(i/20)) + ' ' + str(datetime.datetime.now()) + " ====== \n")

			# check next existed
			next = soup.find('span', {'class':'next'})
			if next != None:
				next_a = next.find('a')
				if next_a is None:
					print('\n ' + name + ' : end at ' + str(i))
					continue

			time.sleep(1)
		except urllib.error.URLError as e: 
			print('code: ' + str(e.code) + ' ; reason: ' + str(e.reason))
			if e.code == 403:
				time.sleep(30)
			ResponseData = e.read().decode("utf8", 'ignore')
		except Exception:
			print('get Exception.')
			print(sys.exc_info())
			pass
	fout.close()
	time.sleep(5)