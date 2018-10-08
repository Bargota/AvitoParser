import requests
from bs4 import BeautifulSoup
import re #импорт модуля регулярных выражений
import csv
import avito
import GoogleSheets


TEST=0


def GetHTMLText(url):
    r=requests.get(url)
    return r.text

def GetTotalPages(html):
    soup = BeautifulSoup(html)
    total_pages = soup.find('div', class_='b-pager').find('ul',class_='e-pages').find_all('a')[6].text
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
    return round(price_m2,2)

def import_csv(data):
    with open ('avito_domofond.csv','a') as f:
        writer = csv.writer(f)
        data['title'] =  data['title'].replace('м²','м2')
        data['price_m2'] =  data['price_m2'].replace('м²','м2')
        data['address'] =  data['address'].replace('−','-')
        writer.writerow((
                         data['title'],
                         data['price'],
                         data['price_m2'],
                         #str(data['area']),
                         data['address'],
                         data['urlad']
                         #str(data['floors']),
                         #data['type_house'],
                         #data['date_ad']
                         ))

def import_Google_Sheet(data):
	data['title'] =  data['title'].replace('м²','м2')
	#data['price_m2'] =  data['price_m2'].replace('м²','м2')
	data['address'] =  data['address'].replace('−','-')

	gs = GoogleSheets.myGoogleSheet()
	data_main_list=[
				   [data['title']],
                   [data['price']],
                   [data['price_m2']],
                   #[str(data['area'])],
                   [data['address']],
                   [data['urlad']]
                   #[str(data['floors'])],
                   #[data['type_house']],
                   #[data['date_ad']]
				   ]
	gs.AppendRow('Лист1!A1',data_main_list)


def import_Google_Sheet_all_data(list):
	all_data=[]
	for i in list:
		i['title'] =  i['title'].replace('м²','м2')
		#i['price_m2'] =  i['price_m2'].replace('м²','м2')
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
	gs.AddData('Лист1!A1',all_data)





def Floors(str):
    floor = re.find_all(r'/(\d{1,2}) эт.',str)
    float_floor  = float(floor[0])
    return float_floor

def GoodAddress(str):
    is_good = ('Площадь Тукая','Суконная слобода','Кремлёвская','Аметьево','Горки')
    for tmp in is_good:
        if tmp in str:
            return True        
    return False

def GetTotalPages(html):
    soup = BeautifulSoup(html)
    tmp_pages = soup.find('div', class_='b-pager').find('ul',class_='e-pages').find_all('li')[-1].text
    #total_pages = tmp_pages.split('=')[1]
    #total_pages = tmp_pages.split('=')[1].split('&')[0]
    return int(tmp_pages)

def ConectLists(list1,list2):
	if len(list1)>len(list2):
		for i in list2:
			list1.append(i)
		return list1
	else:
		for i in list1:
			list2.append(i)
		return list2

def SortListByAddress(list):
	bad_list=['минская','авиастроительный']
	good_list = [
				 #'ул','пер','пр',
                 'толбухина',
                 'гвардейская',
                 'седова','шуртыгина',
                 'сахарова','стрелков',
                 'даурская','такташ',
                 'отрадная','курчатова',
                 'гастелло','товарищеская',
                 'абсалямова','лумумбы',
                 'кутуя']
	final_list=[]
	for i in list:
		sum_find=0
		flag_continue=0
		address_in_lower_case = i['address'].lower()
		for item_bad_list in bad_list:
			finder_bad = address_in_lower_case.find(item_bad_list)	
			if finder_bad>0:
				#list.remove(i)
				flag_continue=1
				continue
			
		if flag_continue==1:
			continue

		for item_good_list in good_list:			
			finder = address_in_lower_case.find(item_good_list)			
			if finder>=0:
				sum_find=sum_find+1
			if sum_find>0:
				continue
		if sum_find==0:
			continue
		final_list.append(i)
	return final_list







#url='https://www.domofond.ru/prodazha-nedvizhimosti/search?MetroIds=289%2C292%2C293%2C290%2C291&PropertyTypeDescription=kvartiry&PriceFrom=2000000&PriceTo=3000000&Rooms=One%2CTwo&Page=1' #однокомнатные и двухкомнатные
#base_url = 'https://www.domofond.ru/prodazha-nedvizhimosti/search?MetroIds=289%2C292%2C293%2C290%2C291&PropertyTypeDescription=kvartiry&PriceFrom=2000000&PriceTo=3000000&Rooms=One%2CTwo&Page='
#https://www.domofond.ru/prodazha-nedvizhimosti/search?MetroIds=296%2C289%2C292%2C293%2C290%2C291&PropertyTypeDescription=kvartiry&PriceFrom=2000000&PriceTo=3100000&Rooms=One&FloorSizeFrom=32&Page=1&SortOrder=PricePerSquareMeterLow&DistanceFromMetro=UpTo3000m
url_base='https://www.domofond.ru/prodazha-nedvizhimosti/search?MetroIds=296%2C289%2C292%2C293%2C290%2C291&PropertyTypeDescription=kvartiry&PriceFrom=2000000&PriceTo=3100000&Rooms=One&FloorSizeFrom=32&Page='

url_second_part='&SortOrder=PricePerSquareMeterLow&DistanceFromMetro=UpTo3000m'
html = GetHTMLText(url_base+str(1)+url_second_part)
total_pages = GetTotalPages(html)
#total_pages = GetTotalPages(GetHTMLText(url))

list=[]

#for i in range(1,total_pages):
count=1


if TEST==1:
	begin_page = 7
	total_pages=8
else:
	begin_page = 1


for i in range(begin_page,total_pages+1):
    
    #url_gen = base_url+str(i) #однокомнатные и двухкомнатные
    html = GetHTMLText(url_base+str(i)+url_second_part)
    soup = BeautifulSoup(html)
    ads= soup.find('div',class_='g-padding-bottom-lg').find_all('div',class_='b-results-tile')
    
    for j in ads:
        description = j.find('div',class_='media').find('div',class_='media-body').find('object')
        try:
            address = description.find('a').find('span',class_='e-tile-address').text.strip()
        except:
            address=""
        try:
            price = description.find('a').find('h2',class_='e-tile-price').text.strip()
            price = price.replace(' РУБ.','')
        except:
            price=""
        try:
            price_m2_str = description.find('a').find('div',class_='e-price-breakdown').text.strip()
            price_m2_str = price_m2_str.replace(' РУБ. за м²','')
            price_m2_str = price_m2_str.replace('\xa0','')
            price_m2=int(price_m2_str )
        except:
            price_m2=0
        try:
            title = description.find('a').find('span',class_='e-tile-type').find('strong').text.strip()
        except:
            title=""
        try:
            url_ad = 'https://www.domofond.ru'+description.find('a').get('href')
        except:
            url_ad=""
        data = {
            'title':title,
            'price':price,
            'price_m2':price_m2,
            #'area':area,
            'address':address,
            'urlad':url_ad,
            #'floors':floors,
            #'date_ad':date_ad,
            #'type_house':type_house}
            }
        if int(price_m2)>65000 and int(price_m2)<85000:
            list.append(data)
        print (str(count)+' '+title+'    '+str(price_m2))        
        count=count+1

avito_list=avito.main(TEST)
united_list = ConectLists(list,avito_list)

sort_list=SortListByAddress(united_list)

import_Google_Sheet_all_data(sort_list)
#for i in list:
#    #import_csv(i)
#	import_Google_Sheet(i)
print('end domofond')



                 
        







       