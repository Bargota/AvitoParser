import requests
from bs4 import BeautifulSoup
#import re #импорт модуля регулярных выражений
#import csv
#import GoogleSheets
import BaseParser
from datetime import datetime, date, time,timedelta
import re


class AvitoParser(BaseParser.Parser):
    
    def GetTotalPages(self,html):
        soup = BeautifulSoup(html,'lxml')
        div = soup.find('div', class_='js-pages')
        span_arr=div.find_all('span', class_='pagination-item-1WyVp')
        span=span_arr[-2].text
        #total_pages = tmp_pages.split('=')[1]
        #self.total_pages = tmp_pages.split('=')[1].split('&')[0]
        self.total_pages = span
        self.total_pages =int(self.total_pages)
        return self.total_pages

    def GetData(self,TEST=0):
                
        self.TestOrNot(TEST)
        print ('avito')
        count=1
        for i in range(self.begin_page,self.total_pages+1):	            
            html = GetHTMLText(self.url+'&p='+str(i))
            soup = BeautifulSoup(html,'lxml')

            ads=self.FindAdsInPage(soup,'div','js-catalog_serp',
                                   'div','item_table')
            print (count)
            for j in ads:
                title=self._FindTitle(j)
                price=self._FindPrice(j)
                url_ad = self._FindUrl(j)
                address = self._FindAddress(j)
                area  = self._FindArea(title)
                price_m2=self._FindPriceM2(price,area)
                floors = self._FindFloors(title)
                date = self._FindDate(j)
                year,found_addres = self._FindYear(address)
                delta_day=(datetime.today()-date).days
                #if delta_day>=2:
                #    return self.list
                

                
                data = {'title':title,
                        'price':price,
                        'price_m2':price_m2,
                        'address':address,
                        'urlad':url_ad,
                        'area':area,
                        'floors':floors,
                        'year':year,
                        'found_addres':found_addres,
                        'date':date
                        #'date_ad':date_ad
                        }
                self.list.append(data)                
                #print(str(count)+' '+data['title']+' '+data['address']+' '+str(data['price'])+'Руб.')  
                print(str(count)+' '+data['date'].strftime("%d.%m.%Y")+' '+str(data['price'])+'Руб.')  
            
            count=count+1        
        #self.list=self._SortRepeat()
        return self.list

    def _FindTitle(self,soup):
        try:
            #title = soup.find('div',class_='description').find('span').text
            h3 = soup.find('h3',class_='snippet-title')
            a=h3.find('a',class_='snippet-link')
            title_text=a.text 
            #print(title_text)           
        except:
            title_text=''
        return title_text

    def _FindPrice(self,soup):
        try:
           #price_str = soup.find('div',class_='description').find('div',class_='about').find('span',class_='price').text.strip()
            price_str= soup.find('div',class_='snippet-price-row').find('span',class_='snippet-price').text.strip()            
            price_str= price_str.replace(' ' , '')
            price_str=price_str[:-1]
            #print(price_str)
            price = int(price_str)

        except:
            price=-1
        return price

    def _FindDate(self,soup):
        try:
            #address = soup.find('div',class_='description').find('p',class_='address').text.strip()
            date0 = soup.find('div',class_='description').find('div',class_='data')
            date_str=date0.find('div',class_='snippet-date-info').text.strip()
            num1= date_str.find('час')
            num2= date_str.find('мин')
            if num1>0 or num2>0:
                date=datetime.today()
                #date=date.strftime("%d.%m.%Y")
            else:
                #d = datetime.today() - timedelta(days=days_to_subtract)
                num3 = re.findall(r'(\d{1,2}) д',date_str)
                if not(len(num3)==0):
                    date = datetime.today() - timedelta(days=int(num3[0]))
                else:
                    date = datetime.strptime("1/1/20 00:00", "%d/%m/%y %H:%M")
        except:
            date=datetime.strptime("1/1/19 00:00", "%d/%m/%y %H:%M") 
        return date
         
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
            url ='https://www.avito.ru'+ soup.find('div',class_='snippet-title-row').find('h3').find('a').get('href')
        except:
            url=''
        return url

    def _FindAddress(self,soup):
        try:
            #address = soup.find('div',class_='description').find('p',class_='address').text.strip()
            address = soup.find('div',class_='description').find('div',class_='item-address').find('span',class_='item-address__string').text.strip()
        except:
            address=''
        return address

    #def _SortRepeat(self):
    #    self.list=sorted(self.list,key= lambda d: d['address'])
    #    for i in range(len(self.list)):
    #        if self.list[i]==self.list[i+1]:
    #            self.list.remove(i)







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


       