import requests
from bs4 import BeautifulSoup
import re #������ ������ ���������� ���������

import BaseParser


class Cian(BaseParser.Parser):
	def GetTotalPages(self,html):    
		self.total_page=''
		while self.total_page=='' or self.total_page=='..':
			soup = BeautifulSoup(html)
			tmp = soup.find('div', id='frontend-serp').find('ul',class_='_93444fe79c-list--35Suf').find_all('li', class_='_93444fe79c-list-item--2QgXB')[-1]
			self.total_page=tmp.text
			if self.total_page=='..':
				url='https://www.cian.ru'+tmp.find('a').get('href')
				try:
					r=requests.get(url)
					html = r.text
				except:
					self.total_page='10'
		self.total_page=int(self.total_page)
		return self.total_page

	def GetData(self):
		#url='https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&in_polygon%5B1%5D=49.084_55.7932%2C49.0929_55.7888%2C49.1002_55.784%2C49.1067_55.7791%2C49.1139_55.7747%2C49.1201_55.7698%2C49.1297_55.7675%2C49.1407_55.7658%2C49.1468_55.7609%2C49.152_55.7559%2C49.162_55.754%2C49.1726_55.7553%2C49.1826_55.7582%2C49.1901_55.7623%2C49.198_55.7665%2C49.2032_55.7716%2C49.2141_55.7735%2C49.2248_55.7737%2C49.2347_55.7753%2C49.2358_55.7811%2C49.2265_55.7849%2C49.2159_55.7851%2C49.2052_55.7845%2C49.1942_55.7849%2C49.1839_55.7865%2C49.175_55.7898%2C49.1692_55.795%2C49.162_55.7998%2C49.1537_55.8037%2C49.1451_55.807%2C49.1345_55.8072%2C49.1238_55.8064%2C49.1129_55.8054%2C49.1026_55.8043%2C49.106_55.8099%2C49.1039_55.8159%2C49.1015_55.8217%2C49.0954_55.8267%2C49.0868_55.83%2C49.0772_55.8275%2C49.0761_55.8217%2C49.0844_55.8174%2C49.0909_55.8128%2C49.0957_55.8076%2C49.094_55.8018%2C49.0885_55.7967&maxprice=3100000&minprice=2000000&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&quality=1&room1=1&room2=1&sort=price_square_order'
		self.GetTotalPages(self.GetHTMLText(self.url))
		print('total_page='+str(self.total_page))
		begin_page=1
		for page in range(begin_page,self.total_page):
			print(page)
			soup = BeautifulSoup(self.GetHTMLText(self.url +'&p='+str(page)))
			#try:
			#	ads = soup.find('div',class_='_93444fe79c-wrapper--1Z8Nz').find_all('div',class_='_93444fe79c-card--2Jgih')
			#except:
			#	ads = []
			ads=self.FindAdsInPage(soup,'div','_93444fe79c-wrapper--1Z8Nz',
								   'div','_93444fe79c-card--2Jgih')

			for item in ads:
				title=self._FindTitle(item)
				price=self._FindPrice(item)
				url_ad = self._FindUrl(item)
				address = self._FindAddress(item)
				area  = self._FindArea(title)
				price_m2=self._FindPriceM2(price,area)


				dict_ad = {'title':title,
							'price':price,
							'price_m2':price_m2,
							'address':address,
							'urlad':url_ad,
							'area':area,
							#'floors':floors,
							#'date_ad':date_ad,
							#'type_house':type_house}
							}
				self.list.append(dict_ad)

	def _FindTitle(self,soup):
		try:
			title = soup.find('div',class_='c6e8ba5398-info-section--28o47 c6e8ba5398-main-info--Rfnfh').find('div',class_='c6e8ba5398-title--3WDDX').text
		except:
			title=''
		return title

	def _FindPrice(self,soup):
		try:
			price_str = soup.find('div',class_='c6e8ba5398-info-section--28o47 c6e8ba5398-main-info--Rfnfh').find('div',class_='c6e8ba5398-header--6WXYW').text
			price = int(price_str.replace(' ','').replace('₽',''))
		except:
			price=0
		return price

	def _FindUrl(self,soup):
		try:
			url = soup.find('div',class_='c6e8ba5398-info-section--28o47 c6e8ba5398-main-info--Rfnfh').find('a').get('href')
		except:
			url=''
		return url

	def _FindAddress(self,soup):
		try:
			address = soup.find('div',class_='c6e8ba5398-address-links--1I9u5').find('span').get('content')
		except:
			address=''
		return address

	def _FindArea(self,title_str):
		area = re.findall(r'(\d{2}.?\d?) м²',title_str)
		float_area  = float(area[0])
		return float_area

	def _FindPriceM2(self,price,area):
		return round(price/area,0)


		
		
	def PrintAllData(self):
		print(self.total_page)
		for i in self.list:			
			print(i['title']+' '+str(i['price'])+'руб. ')


#myC = Cian('https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&in_polygon%5B1%5D=49.084_55.7932%2C49.0929_55.7888%2C49.1002_55.784%2C49.1067_55.7791%2C49.1139_55.7747%2C49.1201_55.7698%2C49.1297_55.7675%2C49.1407_55.7658%2C49.1468_55.7609%2C49.152_55.7559%2C49.162_55.754%2C49.1726_55.7553%2C49.1826_55.7582%2C49.1901_55.7623%2C49.198_55.7665%2C49.2032_55.7716%2C49.2141_55.7735%2C49.2248_55.7737%2C49.2347_55.7753%2C49.2358_55.7811%2C49.2265_55.7849%2C49.2159_55.7851%2C49.2052_55.7845%2C49.1942_55.7849%2C49.1839_55.7865%2C49.175_55.7898%2C49.1692_55.795%2C49.162_55.7998%2C49.1537_55.8037%2C49.1451_55.807%2C49.1345_55.8072%2C49.1238_55.8064%2C49.1129_55.8054%2C49.1026_55.8043%2C49.106_55.8099%2C49.1039_55.8159%2C49.1015_55.8217%2C49.0954_55.8267%2C49.0868_55.83%2C49.0772_55.8275%2C49.0761_55.8217%2C49.0844_55.8174%2C49.0909_55.8128%2C49.0957_55.8076%2C49.094_55.8018%2C49.0885_55.7967&maxprice=3100000&minprice=2000000&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&quality=1&room1=1&room2=1&sort=price_square_order')
##myC.GetTotalPages(myC.GetHTMLText(myC.url))
#myC.GetData()
#myC.PrintAllData()