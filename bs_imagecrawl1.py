import urllib.request
import shutil
import requests
from bs4 import BeautifulSoup
import json
import os


################### image crawling module ####################


def imgdown(url,name,count):

	try:
		# User-Agent를 통해 웹 브라우저 접근 방식으로 http request
		headers = {'User-Agent':'Mozilla/5.0'}
		req = urllib.request.Request(url, None, headers)
		data = urllib.request.urlopen(req).read()

		
		# beautifulsoup로 img 태그를 불러옴
		bs = BeautifulSoup(data,'html.parser')
		img = bs.find_all('img')
		clothUrlList = []
		modelUrlList = []
		
		for ele in img:
			val = ele.get('class')
			if val != None and ele.get("data-altimage") != None: 
				cloth_url = ele.get("src")	#이미지 소스
				model_url = ele.get("data-altimage") # 착용샷 소스
				#print(type(cloth_url))
				#print(cloth_url)
				cloth_url = cloth_url.replace("style", "fullscreen")
				model_url = model_url.replace("main", "fullscreen")
				clothUrlList.append(cloth_url)
				modelUrlList.append(model_url)
		print(len(clothUrlList))


		print("#")
		
		imgpath= "./IMGcrawl/" + name + "/"
		if not os.path.isdir(imgpath):
			os.makedirs(imgpath)
		print("#")		
		imgpath_org = imgpath + 'original/'
		if not os.path.isdir(imgpath_org):
			os.makedirs(imgpath_org)
		print("#")
		imgpath_model = imgpath + 'model/'
		if not os.path.isdir(imgpath_model):
			os.makedirs(imgpath_model)
		
		print("#")
		print(len(clothUrlList))
		start = count * 30

		# http request가 필요한 사이트는 urllib.request.urlretrieve()를 사용하지 못함
		# 따라서 객체를 복사해서 저장하는 방식으로 진행
		for i in range(start, len(clothUrlList)):
			print(start)
			clothName = str(start).zfill(6) + "_1.png"
			modelName = str(start).zfill(6) + "_0.png"
			r_cloth = requests.get('http:' + clothUrlList[start], stream = True, headers = headers)
			r_model = requests.get('http:' + modelUrlList[start], stream = True, headers = headers)
			if r_cloth.status_code == 200:
				with open(imgpath_org + clothName, 'wb') as f_cloth:
					r_cloth.raw.decode_content = True
					shutil.copyfileobj(r_cloth.raw, f_cloth)
			if r_model.status_code == 200:
				with open(imgpath_model + modelName, 'wb') as f_model:
					r_model.raw.decode_content = True
					shutil.copyfileobj(r_model.raw, f_model)
			start = start + 1
		# list 초기화
		del clothUrlList
		del modelUrlList
		#urllib.request.urlretrieve("http:" + clothUrlList[0], imgpath_org+imgname) #이미지 로컬에 다운로드 
		#urllib.request.urlretrieve("http:" + modelUrlList[0], imgpath_model+imgname)
	except Exception as e:
		print("error! : %s" % e)
		return -1
	return 1



################### 상세페이지 URL 따는 파트 ####################
def UrlLoad(lines):
	f = open("siteinfo.txt", 'r')
	lines = f.read().split('\n')
	return lines

lines = []
lines = UrlLoad(lines)


for line in lines:
	data = line.split(',')
	name, url, pageSize = data[0], data[1], data[2]
	try:
		urlList = []
		# H&M 은 30장씩 끊어서 페이지가 나뉘어져 있음
		for i in range(30, int(pageSize) + 1, 30): #30 ~ 240
			print(i)
			urlStr = url + str(i)
			print(urlStr)
			urlList.append(urlStr)

		
		f = open("test2.txt","a")
		count = 0
		for item in urlList:
			f.write(item)
			f.write('\n')
			if(imgdown(item, name, count)==-1):
				exit()
				print("\n\n*ERROR*\n\n")
			else:
				count = count + 1
		f.close()
		
	except Exception as e:
		print("\n\n____________ERROR___________\n\n")
		print("The error is: %s" % e)
