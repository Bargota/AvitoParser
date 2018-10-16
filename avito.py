import requests
from bs4 import BeautifulSoup
#import re #импорт модуля регулярных выражений
#import csv
#import GoogleSheets
import BaseParser


class AvitoParser(BaseParser.Parser):
	
	def GetTotalPages(self,html):
		soup = BeautifulSoup(html,'lxml')
		tmp_pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
		#total_pages = tmp_pages.split('=')[1]
		self.total_pages = tmp_pages.split('=')[1].split('&')[0]
		self.total_pages =int(self.total_pages)
		return self.total_pages

	def GetData(self,TEST=0):
		base_url = 'https://www.avito.ru/kazan/kvartiry/prodam?'
		page_url = 'p='
		
		self.TestOrNot(TEST)
		
		count=1
		for i in range(self.begin_page,self.total_pages+1):	
			#url_gen = base_url+page_url+str(i)+'&f=549_5696-5697'
			url_gen = base_url+page_url+str(i)+'&pmax=3100000&pmin=2000000&f=59_13987b0.497_0b5196'
			
			html = GetHTMLText(url_gen)
			soup = BeautifulSoup(html,'lxml')

			ads=self.FindAdsInPage(soup,'div','catalog-list',
								   'div','item_table')

			for j in ads:
				title=self._FindTitle(j)
				price=self._FindPrice(j)
				url_ad = self._FindUrl(j)
				address = self._FindAddress(j)
				area  = self._FindArea(title)
				price_m2=self._FindPriceM2(price,area)
				floors = self._FindFloors(title)
			
				try:
					date_ad=description.find('div',class_='data').find('div').get('data-absolute-date')            
				except:
					date_ad='' 

				
				data = {'title':title,
						'price':price,
						'price_m2':price_m2,
						'address':address,
						'urlad':url_ad,
						'area':area,
						'floors':floors,
						#'date_ad':date_ad
						}
				self.list.append(data)
				print(str(count)+' '+data['title']+' '+data['address']+' '+str(data['price']))
				count=count+1
		return self.list

	def _FindTitle(self,soup):
		try:
			title = soup.find('div',class_='description').find('span').text
		except:
			title=''
		return title

	def _FindPrice(self,soup):
		try:
			price_str = soup.find('div',class_='description').find('div',class_='about').find('span',class_='price').text.strip()
			price_str= price_str.replace(' ' , '')
			price_str=price_str[:-1]
			price = int(price_str)
		except:
			price=-1
		return price
		 
	#def _FindArea(self,title_str):
	#	area = re.findall(r'(\d{2}.?\d?) м²',title_str)
	#	float_area  = float(area[0])
	#	return float_area

	#def _FindPriceM2(self,price,area):
	#	return round(price/area,0)

	#def _FindFloors(self,title_str):
	#	floor = re.findall(r'/(\d{1,2}) эт.',title_str)
	#	float_floor  = int(floor[0])
	#	return float_floor

	def _FindUrl(self,soup):
		try:
			url ='https://www.avito.ru'+ soup.find('div',class_='description').find('h3').find('a').get('href')
		except:
			url=''
		return url

	def _FindAddress(self,soup):
		try:
			address = soup.find('div',class_='description').find('p',class_='address').text.strip()
		except:
			address=''
		return address







def GetHTMLText(url):
	try:
		r=requests.get(url)
	except:
		return ''
	return r.text

def GetTotalPages(html):
	soup = BeautifulSoup(html,'lxml')
	tmp_pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
	#total_pages = tmp_pages.split('=')[1]
	total_pages = tmp_pages.split('=')[1].split('&')[0]
	return int(total_pages)

def Price2Float(str):
	str = str.replace(' ' , '')
	str=str[:-1]
	return round(float(str))

def FlatArea(str_title):
	area = re.findall(r'(\d{2}.?\d?) м²',str_title)
	float_area  = float(area[0])
	return float_area

def Price1m2(flat_price,area):
	price_m2=flat_price/area
	return round(price_m2)

def import_csv(data):
	with open ('avito_domofond.csv','a') as f:
		writer = csv.writer(f)
		data['title'] =  data['title'].replace('м²','м2')
		data['address'] =  data['address'].replace('−','-')
		writer.writerow((data['title'],
						 str(data['price']),
						 str(data['price_m2']),
						 data['address'],
						 data['urlad'],
						 str(data['area']),
						 str(data['floors']),
						 #data['type_house'],
						 data['date_ad']
						 ))

def import_Google_Sheet_all_data(list):
	all_data=[]
	for i in list:
		i['title'] =  i['title'].replace('м²','м2')
		i['address'] =  i['address'].replace('−','-')

		row_list=[
				   i['title'],
				   i['price'],
				   i['price_m2'],
				   #str(data['area']),
				   i['address'],
				   i['urlad']
				   #str(data['floors']),
				   #data['type_house'],
				   #data['date_ad']
				   ]
		all_data.append(row_list)
	gs = GoogleSheets.myGoogleSheet()
	#gs.AppendRow('Лист1!A1',all_data)
	gs.AddData('Лист1!A1000',all_data)

def Floors(str):
	floor = re.findall(r'/(\d{1,2}) эт.',str)
	float_floor  = float(floor[0])
	return float_floor

def GoodAddress(str):
	is_good = ('Площадь Тукая','Суконная слобода','Кремлёвская','Аметьево','Горки')
	for tmp in is_good:
		if tmp in str:
			return True        
	return False


def main(TEST):
	##url = 'https://www.avito.ru/kazan/kvartiry/prodam/1-komnatnye?p=1'  #однокомнатные
	##base_url = 'https://www.avito.ru/kazan/kvartiry/prodam/1-komnatnye?'

	url='https://www.avito.ru/kazan/kvartiry/prodam?p=1&f=549_5696-5697' #однокомнатные и двухкомнатные
	base_url = 'https://www.avito.ru/kazan/kvartiry/prodam?'

	##url = 'https://www.avito.ru/kazan/avtomobili?radius=200&s_trg=3&i=1' #машины
	##base_url = 'https://www.avito.ru/kazan/avtomobili?'

	page_url = 'p='
	total_pages = GetTotalPages(GetHTMLText(url))

	list=[]
	counter=1

	if TEST==1:
		begin_page=1
		total_pages=2
	else:
		begin_page=1

	for i in range(begin_page,total_pages+1):

	
		#url_gen = base_url+page_url+str(i) #однокомнатные
		url_gen = base_url+page_url+str(i)+'&f=549_5696-5697' #однокомнатные и двухкомнатные
		html = GetHTMLText(url_gen)
		soup = BeautifulSoup(html,'lxml')
		ads= soup.find('div',class_='catalog-list').find_all('div',class_='item_table')
		#ads= soup.find('div',class_='catalog-list').find_all('div',class_='item')
		
		for j in ads:
			description = j.find('div',class_='description')
			try:
			
				title = description.find('span').text           
				counter=counter+1
				print(str(i)+'  '+str(counter)+"    "+title)
				floors = Floors(title)
				area = FlatArea(title)
			except:
				title=""
				floors=0
				area=0            
			try:
				price = description.find('div',class_='about').find('span',class_='price').text.strip()
				price = Price2Float(price)  
				if area!=0:
					price_m2 = Price1m2(price,area)
			except:
				price=-1
				price_m2=0
			try:
				address = description.find('p',class_='address').text.strip()
				is_good_address = GoodAddress(address)
			except:
				address=""
				is_good_address=False
			try:
				url_ad='https://www.avito.ru'+description.find('h3').find('a').get('href')
			
			except:
				url_ad='' 
			
			try:
				date_ad=description.find('div',class_='data').find('div').get('data-absolute-date')            
			except:
				date_ad='' 
			
			
			if   area>32 and is_good_address and price_m2>65000 and price_m2<85000:
				 #html_ad=GetHTMLText(url_ad)
				 #if html_ad!='' :
				 #   soup_html_ad=BeautifulSoup(html_ad)
				 #   try:
				 #       type_house = soup_html_ad.find('div', class_='item-params').find_all('span',class_='item-params-label')[3].next_sibling.strip()
				 #   except:
				 #       type_house=''
				 #   if type_house=='кирпичный' :
				data = {'title':title,
						'price':price,
						'price_m2':price_m2,
						'address':address,
						'urlad':url_ad,
						'area':area,
						'floors':floors,
						'date_ad':date_ad,
						#'type_house':type_house}
						}
				#import_csv(data)
				print('OK')
				list.append(data)

	list=sorted(list, key=lambda x: x['price'])
	print('sort')

	#import_Google_Sheet_all_data(list)
	#for i in list:
	#    import_csv(i)
	
	print('end avito')
	return list


#main(1)


	   