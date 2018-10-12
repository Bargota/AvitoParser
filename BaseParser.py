import requests
import re



class Parser():
	def __init__(self,url):
		self.url=url
		self.total_pages=0
		self.begin_page=0
		self.list = []

	def GetHTMLText(self,url):
		try:
			r=requests.get(url)
		except:
			return ''
		return r.text

	def TestOrNot(self,TEST=0):
		if TEST==1:
			self.total_pages=2
			self.begin_page=1
		else:
			self.GetTotalPages(self.GetHTMLText(self.url))
			print('total_page='+str(self.total_pages))
			self.begin_page=1

	def FindAdsInPage(self,soup,key,class_,key_all,class_all):
		try:
			ads = soup.find(key,class_=class_).find_all(key_all,class_=class_all)
		except:
			ads = []
		return ads

	def _FindArea(self,title_str):
		area = re.findall(r'(\d{2}.?\d?) м²',title_str)
		float_area  = float(area[0])
		return float_area

	def _FindPriceM2(self,price,area):
		return round(price/area,0)

	def _FindFloors(self,title_str):
			floor = re.findall(r'/(\d{1,2}) эт.',title_str)
			floors  = int(floor[0])
			return floors