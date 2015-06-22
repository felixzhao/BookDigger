#encoding:UTF-8
import requests
import time
import datetime
import sys
from bs4 import BeautifulSoup
import re

import codecs

from Tkinter import *

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
	#fout = open('../Comments.txt','w', 'utf-8')
	fout = codecs.open('Comments.txt','w',encoding='UTF-8')

	listbox.insert(END,' ### Start Get Comments. ### ')
	url_path = url + 'comments/hot?p='

	page_num = 1
	try:
		page_count = getPageCount(url_path + str(page_num))
		if page_count is None or page_count == 0:
			listbox.insert(END,'No data need to dig.')
			return
		else:
			listbox.insert(END,' !!! total page : ' + str(page_count))
		while True:
			listbox.insert(END,' >>> Start Page : ' + str(page_num))
			url = url_path + str(page_num)

			soup = getSoup(url)
			infos = soup.findAll('li',{'class':'comment-item'})
			if infos is not None and len(infos) > 0:
				for info in infos:
					comment = info.find('p',{'class':'comment-content'})
					if comment is not None:
						content = comment.string
#						content = unicode(comment.string.content.strip(codecs.BOM_UTF8), 'utf-8')
#						parser.parse(StringIO.StringIO(content))
						listbox.insert(END,' >>> ' + content.encode("utf-8"))
						fout.write(content + '\n')
						fout.write

			if checkNext(page_num, page_count) == True:
				page_num += 1
				listbox.insert(END,' >>> Page Done : ' + str(page_num))
			else:
				fout.close()
				listbox.insert(END," ### Get Comments Done at page : " + str(page_num) + " Total : " + str(page_count) + " ### ")
				return
			time.sleep(1)
			pass
	except Exception:
			listbox.insert(END,'get Exception.')
			listbox.insert(END,sys.exc_info())
			pass

def Call():
    button_submit['bg'] = 'blue'
    button_submit['fg'] = 'white'

    url = input_url.get()
    listbox.insert(END,'Start dig from ' + url);
    getComments(url)
    

root = Tk()
root.geometry('800x600+350+70')
label_url = Label( root, text="Please input source url:")
input_url = Entry(root, bd =1)
button_submit = Button(root, text = 'Start', command = Call)
#listbox = Listbox(root)
#listbox.autowidth(250)

scrollbar = Scrollbar(root, orient="vertical")
listbox = Listbox(root, width=50, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

scrollbar.pack(side="right", fill="y")
listbox.pack(side="right",fill="both", expand=True)

label_url.pack()
input_url.pack()
button_submit.pack()
listbox.pack()   

root.mainloop()