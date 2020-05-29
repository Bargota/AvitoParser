import requests
from bs4 import BeautifulSoup
#import re #импорт модуля регулярных выражений
#import csv
#import avito
#import GoogleSheets
#import Cian
import BaseParser
#import WorkLists
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


def GetHTMLText(url):
    r=requests.get(url)
    return r.text

def GetTotalPages(html):
    soup = BeautifulSoup(html,'lxml')
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
    soup = BeautifulSoup(html,'lxml')
    tmp_pages = soup.find('div', class_='b-pager').find('ul',class_='e-pages').find_all('li')[-1].text
    #total_pages = tmp_pages.split('=')[1]
    #total_pages = tmp_pages.split('=')[1].split('&')[0]
    return int(tmp_pages)









def main():
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
        soup = BeautifulSoup(html,'lxml')
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

    print('end domofond')

    avito_list=avito.main(TEST)
    united_list =WorkLists.ConectLists(list,avito_list)



    myC = Cian.Cian('https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&in_polygon%5B1%5D=49.084_55.7932%2C49.0929_55.7888%2C49.1002_55.784%2C49.1067_55.7791%2C49.1139_55.7747%2C49.1201_55.7698%2C49.1297_55.7675%2C49.1407_55.7658%2C49.1468_55.7609%2C49.152_55.7559%2C49.162_55.754%2C49.1726_55.7553%2C49.1826_55.7582%2C49.1901_55.7623%2C49.198_55.7665%2C49.2032_55.7716%2C49.2141_55.7735%2C49.2248_55.7737%2C49.2347_55.7753%2C49.2358_55.7811%2C49.2265_55.7849%2C49.2159_55.7851%2C49.2052_55.7845%2C49.1942_55.7849%2C49.1839_55.7865%2C49.175_55.7898%2C49.1692_55.795%2C49.162_55.7998%2C49.1537_55.8037%2C49.1451_55.807%2C49.1345_55.8072%2C49.1238_55.8064%2C49.1129_55.8054%2C49.1026_55.8043%2C49.106_55.8099%2C49.1039_55.8159%2C49.1015_55.8217%2C49.0954_55.8267%2C49.0868_55.83%2C49.0772_55.8275%2C49.0761_55.8217%2C49.0844_55.8174%2C49.0909_55.8128%2C49.0957_55.8076%2C49.094_55.8018%2C49.0885_55.7967&maxprice=3100000&minprice=2000000&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&quality=1&room1=1&room2=1&sort=price_square_order')
    myC.GetData()
    cian_list = myC.list

    united_list_all = WorkLists.ConectLists(united_list,cian_list)
    sort_list=WorkLists.SortListByAddress(united_list_all )
    sort_list_area=WorkLists.SortListByArea(sort_list,32)

    WorkLists.import_Google_Sheet_all_data(sort_list_area)

#main()




                 
        







       