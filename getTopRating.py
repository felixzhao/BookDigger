#encoding:UTF-8
import requests
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

fcat = open('./catlogos_all.txt','r')

name_list = fcat.readline().split()

for name in name_list:
	fout = open('./rating_out/' + name + '.txt','w')

	#flog = open('../page_content.race','w')

	url_name = str(name.encode('UTF-8'))[2:-1].replace('\\x','%').upper()
	url_root = "http://book.douban.com/tag/" + url_name
	url_path = url_root

	while True:
		print(url_path + ' ' + 'datetime? : ' + str(datetime.datetime.now()))
		try:
			print('\n==>start get page.\n')

			response = requests.get(url_path)
			#headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76'}  
			#req = urllib.request.Request(url_path, headers=headers)
			#page = urllib.request.urlopen(req)

			#page = urllib.request(url_path, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
			#page = urllib.request.urlopen(url_path)

			#data = page.read()
			#data = data.decode('UTF-8')

			#flog.write(response.text)
			#flog.write('\n ======= \n')

			soup = BeautifulSoup(response.text)
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

				if float(rating) > 8.9 and int(pl) > 3000:
					print("### match : " + bookName + ' , ' + rating + ' , ' +  pl + ' , \'' + pub.strip() + '\'')
					fout.write(bookName + ' , ' + rating + ' , ' +  pl + ' , \'' + pub.strip() + '\'')
					fout.write('\n')
			#fout.write("====== page " + str(int(i/20)) + ' ' + str(datetime.datetime.now()) + " ====== \n")
			#print("====== page " + str(int(i/20)) + ' ' + str(datetime.datetime.now()) + " ====== \n")

			# check next existed
			next = soup.find('span', {'class':'next'})
			if next == None:
				print("\n!!! Exception: No Next span !!!\n")
				break

			next_a = next.find('a', href=True)
			if next_a is None:
				print('\n ' + name + ' : end at ' + url_path + ' \n')
				break

			if next_a['href'] == None:
				print("\n!!! Exception: Next Page Url is Empty !!!\n")
				break
			#debug
			print('href : ' + next_a['href'] + '\n')
			page_num = next_a['href'].split('=')[1].split['&'][0]
			print('page num : ' + page_num + '\n')

			next_url_para = "?start=" + str(int(page_num)) + "&type=T" #next_a['href'].split('?')[1]
			url_path = url_root + next_url_para

			print('\n==> end of get page.\n')

			time.sleep(10)
		#except urllib.error.URLError as e: 
		#	print('code: ' + str(e.code) + ' ; reason: ' + str(e.reason))
		#	if e.code == 403:
		#		time.sleep(30)
		#	ResponseData = e.read().decode("utf8", 'ignore')
		except Exception:
			print('get Exception.')
			print(sys.exc_info())
			pass
	fout.close()
	time.sleep(60)