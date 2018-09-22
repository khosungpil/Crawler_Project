import urllib.request
import shutil
import requests
from bs4 import BeautifulSoup
import json
import os

"""
	이번 사이트에는 페이지가 나뉘어져 있지 않고 한 페이지에 전부 데이터가 존재
"""
################### image crawling module ####################
def ModelImageDown(imgpath_model, modelUrlList, headers):
	count = 0
	for model in modelUrlList:
		
		modelName = str(count).zfill(6) + "_1.png"
		r_model = requests.get('https:' + model, stream = True, headers = headers)
		if r_model.status_code == 200:
			with open(imgpath_model + modelName, 'wb') as f_model:
				r_model.raw.decode_content = True
				shutil.copyfileobj(r_model.raw, f_model)
		print("save model: " + str(count) + model)
		count = count + 1
	return 1
def ClothImageDown(imgpath_org, clothUrlList, headers):
	count = 0
	for cloth in clothUrlList:
		print(cloth)
		clothName = str(count).zfill(6) + "_0.png"
		r_cloth = requests.get('https:' + cloth, stream = True, headers = headers)
		if r_cloth.status_code == 200:
			with open(imgpath_org + clothName, 'wb') as f_cloth:
				r_cloth.raw.decode_content = True
				shutil.copyfileobj(r_cloth.raw, f_cloth)
		print("save cloth " + str(count) + cloth)
		count = count + 1
	return 1
def SaveHref(url,name):
	hrefClassList = []
	clothUrlList = []
	modelUrlList = []
	countItem = 0
	# User-Agent를 통해 웹 브라우저 접근 방식으로 http request
	
	try:	
		headers = {'User-Agent':'Mozilla/5.0'}
		req = urllib.request.Request(url, None, headers)
		data = urllib.request.urlopen(req).read()
	except Exception as e:
		print("Error : %s" %e)
		return -1
		
	# beautifulsoup로 a class 태그를 불러옴
	bs = BeautifulSoup(data,'html.parser')
	divClassList = bs.find_all("div", {"class" : "product-info-item product-info-item-name"})

	

	for div in divClassList:
		temp = div.find("a")
		_url = temp["href"]
		hrefClassList.append(_url)
	
	for href in hrefClassList:
		
		# divClass를 리스트로 저장하지 않고 image만 뽑아서 안에 숫자를 바꿔 product image를 추출한다.
		try:
			headers_href = {'User-Agent':'Mozilla/5.0'}
			req_href = urllib.request.Request(href, None, headers_href)
			data_href = urllib.request.urlopen(req_href).read()
		except Exception as e:
			print("Error : %s" %e)
			return -1
		bs_href = BeautifulSoup(data_href, 'html.parser')
		divClassInHref = bs_href.find("div", {"class" : "media-wrap image-wrap"})
		temp2 = divClassInHref.find("a")
		imgUrl = temp2["href"]
		modelUrl = imgUrl
		# 1 : model image, 6 : cloth image
		clothUrl = imgUrl.replace("_1_1_1", "_6_1_1")
		modelUrlList.append(modelUrl)
		clothUrlList.append(clothUrl)
		print("Append " + str(countItem) + " items in UrlLists")
		countItem = countItem + 1
		
	imgpath = "./IMGcrawl/" + name + "/"
	print("# Check the Image path")
	if not os.path.isdir(imgpath):
		os.makedirs(imgpath)
	print("# Check the product folder")
	imgpath_org = imgpath + 'original/'
	if not os.path.isdir(imgpath_org):
		os.makedirs(imgpath_org)
	print("# Check the model folder")
	imgpath_model = imgpath + 'model/'
	if not os.path.isdir(imgpath_model):
		os.makedirs(imgpath_model)

	ClothImageDown(imgpath_org, clothUrlList, headers_href)
	ModelImageDown(imgpath_model, modelUrlList, headers_href)

	del clothUrlList
	del modelUrlList
	del hrefClassList

	return 1
		

# Url을 불러 온다.
def UrlLoad(lines):
	f = open("siteinfo.txt", 'r')
	lines = f.read().split('\n')
	return lines

lines = []
lines = UrlLoad(lines)


for line in lines:
	data = line.split(',')
	name, url = data[0], data[1]
	
	f = open("test2.txt", "a")
	f.write(url + '\n')
	if(SaveHref(url, name) == -1):
		exit()
		print("\n\n*ERROR*\n\n")
	f.close()

