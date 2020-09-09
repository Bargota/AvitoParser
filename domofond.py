import requests
from bs4 import BeautifulSoup
#import re #импорт модуля регулярных выражений
import csv
#import avito
import GoogleSheets
#import Cian
import BaseParser
import WorkLists
from datetime import datetime, date, time

TEST=0

class DomofondParser(BaseParser.Parser):	
    def GetTotalPages(self,html):
        soup = BeautifulSoup(html,'lxml')
        total_pages_str = soup.find('nav', class_='pagination__root___38MdD').find('ul',class_='pagination__mainPages___2v12k').find_all('li')[-1].text        
        self.total_pages = int(total_pages_str)
        return int(self.total_pages)

    def GetData(self,TEST=0):
        
        #base_url='https://www.domofond.ru/prodazha-nedvizhimosti/search?MetroIds=289%2C292%2C293%2C290%2C291&PropertyTypeDescription=kvartiry&PriceFrom=2000000&PriceTo=3200000&Rooms=One%2CTwo&Page='
        #url_second_part='&SortOrder=PricePerSquareMeterLow&DistanceFromMetro=UpTo3000m'
        
        self.TestOrNot(TEST)
        print ('domofond')
        
        for page in range(self.begin_page,self.total_pages+1):
            if TEST==2:
                if page!=self.total_pages:
                    continue
            #url_gen = base_url+str(page)+url_second_part
            url_gen = self.url+"&Page="+str(page)
            print(page)
            soup = BeautifulSoup(self.GetHTMLText(url_gen),'lxml')
            
            ads=self.FindAdsInPage(soup,'div','search-results__itemCardList___RdWje','a','long-item-card__item___ubItG')
                                   
            
            for item in ads:
                title=self._FindTitle(item)
                price=self._FindPrice(item)
                url_ad = self._FindUrl(item)
                address = self._FindAddress(item)
                area  = self._FindArea(title)
                price_m2=self._FindPriceM2(price,area)                
                floor_number,floors = self._FindFloors(title)
                date = self._FindDate(item)
                year,found_addres = self._FindYear(address)

                data = {'title':title,
                            'price':price,
                            'price_m2':price_m2,
                            'address':address,
                            'urlad':url_ad,
                            'area':area,
                            'floor_number':floor_number,
                            'floors':floors,
                            'year':year,
                            'found_addres':found_addres,
                            'date':date
                            #'date_ad':date_ad,
                            #'type_house':type_house}
                            }
                self.list.append(data)
                
                print(str(page)+' '+data['title']+' '+data['address']+' '+str(data['price'])+'Руб.') 
            
        return self.list

    def _FindTitle(self,soup):
        try:
            #title = soup.find('a').find('span',class_='e-tile-type').find('strong').text.strip()
            title = soup.find('div',class_='long-item-card__informationHeaderRight___3bkKw').text.strip()
        except:
            title=''
        return title

    def _FindDate(self,soup):  
        
        try:
            #address = soup.find('div',class_='description').find('p',class_='address').text.strip()
            date_str = soup.find('div',class_='long-item-card__information___YXOtb').find('div',class_='long-item-card__informationFooterRight___3Xw4i').text
            #date_str=date0.find('div',class_='snippet-date-info').text.strip()

            date=self._ParseDate(date_str)
        except:
            date=datetime.strptime("1/1/19 00:00", "%d/%m/%y %H:%M") 
        return date      
        

    def _FindPrice(self,soup):
        try:
            #price_str = soup.find('a').find('h2',class_='e-tile-price').text.strip()
            price_str = soup.find('span',class_='long-item-card__price___3A6JF').text.strip()
            price_str= price_str.replace(' ₽','')
            price_str = price_str.replace(' ','')				
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
           # url ='https://www.domofond.ru'+soup.find('a').get('href')
            url ='https://www.domofond.ru'+soup.get('href')
        except:
            url=''
        return url

    def _FindAddress(self,soup):
        try:
            #address =  soup.find('a').find('span',class_='e-tile-address').text.strip()
            address =  soup.find('div',class_='long-item-card__informationMain___LnRL6').find('span',class_='long-item-card__address___PVI5p').text.strip()
        except:
            address=''
        return address


# def GetHTMLText(url):
#     r=requests.get(url)
#     return r.text

# def GetTotalPages(html):
#     soup = BeautifulSoup(html,'lxml')
#     total_pages = soup.find('div', class_='b-pager').find('ul',class_='e-pages').find_all('a')[6].text
#     return int(total_pages)

# def Price2Float(str):
#     str = str.replace(' ' , '')
#     str=str[:-1]
#     return round(float(str))

# def FlatArea(str_title):
#     area = re.findall(r'(\d{2}.?\d?) м²',str_title)
#     float_area  = float(area[0])
#     return float_area

# def Price1m2(flat_price,area):
#     price_m2=flat_price/area
#     return round(price_m2,2)

# def import_csv(data):
#     with open ('avito_domofond.csv','a') as f:
#         writer = csv.writer(f)
#         data['title'] =  data['title'].replace('м²','м2')
#         data['price_m2'] =  data['price_m2'].replace('м²','м2')
#         data['address'] =  data['address'].replace('−','-')
#         writer.writerow((
#                          data['title'],
#                          data['price'],
#                          data['price_m2'],
#                          #str(data['area']),
#                          data['address'],
#                          data['urlad']
#                          #str(data['floors']),
#                          #data['type_house'],
#                          #data['date_ad']
#                          ))

# def import_Google_Sheet(data):
#     data['title'] =  data['title'].replace('м²','м2')
#     #data['price_m2'] =  data['price_m2'].replace('м²','м2')
#     data['address'] =  data['address'].replace('−','-')

#     gs = GoogleSheets.myGoogleSheet()
#     data_main_list=[
#                    [data['title']],
#                    [data['price']],
#                    [data['price_m2']],
#                    #[str(data['area'])],
#                    [data['address']],
#                    [data['urlad']]
#                    #[str(data['floors'])],
#                    #[data['type_house']],
#                    #[data['date_ad']]
#                    ]
#     gs.AppendRow('Лист1!A1',data_main_list)








# def Floors(str):
#     floor = re.find_all(r'/(\d{1,2}) эт.',str)
#     float_floor  = float(floor[0])
#     return float_floor

# def GoodAddress(str):
#     is_good = ('Площадь Тукая','Суконная слобода','Кремлёвская','Аметьево','Горки')
#     for tmp in is_good:
#         if tmp in str:
#             return True        
#     return False

# # def GetTotalPages(html):
# #     soup = BeautifulSoup(html,'lxml')
# #     tmp_pages = soup.find('div', class_='b-pager').find('ul',class_='e-pages').find_all('li')[-1].text
# #     #total_pages = tmp_pages.split('=')[1]
# #     #total_pages = tmp_pages.split('=')[1].split('&')[0]
# #     return int(tmp_pages)














                 
        







       