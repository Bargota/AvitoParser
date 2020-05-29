import requests
import re
import sys
#sys.path.insert(0, 'P:\\Project\\MyProject\\AvitoParser\\YearOfConstruction\\')
#path_file_streets='P:\\Project\\MyProject\\AvitoParser\\YearOfConstruction\\'
sys.path.insert(0, 'D:\\v.orlov\\Programm\\python\\2\\AvitoParser\\YearOfConstruction\\')
path_file_streets='D:\\v.orlov\\Programm\\python\\2\\AvitoParser\\YearOfConstruction\\'
name_file_streets='streets_list.txt'
from main_for_year import FoundYearFromAddres
from GoogleSheets import myGoogleSheet
from datetime import datetime, date, time,timedelta

class Parser():
    def __init__(self,url):
        self.url=url
        self.total_pages=0
        self.begin_page=0
        self.list = []
        
        #чтение данных из гугл таблицы о адресе и годе постройки
        self.GS_settings_year = myGoogleSheet()
        self.list_addres_and_year =self.GS_settings_year.ReadData('mingkh.ru!B2:E6000')


    

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
            all = soup.find(key,class_=class_)
            ads=all.find_all(key_all,class_=class_all)
        except:
            ads = []
        return ads

    def _FindArea(self,title_str):
        if title_str!="":

            area = re.findall(r'( \d{2}[.,]?\d?) м²',title_str)
            float_area  = float(area[0])
            return float_area
        return 0

    def _FindPriceM2(self,price,area):
        if area!=0:
            return round(price/area,0)
        return 0

    def _FindFloors(self,title_str):
        if title_str!="":
            floor = re.findall(r'(\d{1,3})/(\d{1,3}) эт.',title_str)
           
            floors  = int(floor[0][1])
            floor_number=int(floor[0][0])
            return floor_number,floors
        return 0

    def _FindYear(self,addres_str):
        my_found_year_from_addres=FoundYearFromAddres()
        #path_file_streets='D:\\v.orlov\\Programm\\python\\2\\AvitoParser\\YearOfConstruction\\'
        #name_file_streets='streets_list.txt'
        year = my_found_year_from_addres.FindYearOfConstruction(addres_str,path_file_streets+name_file_streets,self.list_addres_and_year)
        return year,my_found_year_from_addres.street_name +' '+my_found_year_from_addres.house_number

    def _SortRepeat(self,list):
        list=sorted(list,key= lambda d: d['address'])
        final_list=[]
        for i in range(len(list)):
            if i==0:
                final_list.append(list[i])
            else:
                if list[i]['address']!=final_list[-1]['address']:
                    final_list.append(list[i])
        return final_list

    def _WhatInterval(self,reg_exp,interval_str,interval_num,how_many_day=0):
        interval=re.findall(r'('+reg_exp+')',interval_str)
        date=None
        if len(interval)>0:
            date = datetime.today()-timedelta(days=int(interval_num)*how_many_day)
        return date

    def _ParseDate(self,line):    
        word_back=re.findall(r'() назад',line)
        if len(word_back)>0:
            interval_size=re.findall(r'((\d{1,2}) ((недел[юи])|(де?н(ь|(ей)|я))|(час((ов)|а)?)|(минуту?)|(месяц(ев|а))|((года?)|(лет))))',line)
            if len(interval_size)>0:
                date=None
                if (date==None):
                    date=self._WhatInterval('(час((ов)|а)?)|(минуту?)',interval_size[0][2],interval_size[0][1],0)
                if (date==None):
                    date=self._WhatInterval('де?н(ь|(ей)|я)',interval_size[0][2],interval_size[0][1],1)
                if (date==None):
                    date=self._WhatInterval('недел[юи]',interval_size[0][2],interval_size[0][1],7)
                if (date==None):
                    date=self._WhatInterval('месяц(ев|а)',interval_size[0][2],interval_size[0][1],30)
                if (date==None):
                    date=self._WhatInterval('(года?)|(лет)',interval_size[0][2],interval_size[0][1],355)
            else:
                date = datetime.strptime("1/1/11 00:00", "%d/%m/%y %H:%M")
        else:
            list_manth=['январ',
                  'феврал',
                  'март',
                  'апрел',
                  'ма',
                  'июн',
                  'июл',
                  'август',
                  'сентябр',
                  'октябр',
                  'ноябр',
                  'декабр'
                  ]
            #interval_size=re.findall(r'((\d{1,2}) ([А-Яа-я]) )',line)
            interval_size=re.findall(r'((\d{1,2}) (\w{2,7}) )',line)
            if len(interval_size)>0:
                for i in range(len(list_manth)):
                    _manth=re.findall(r'('+list_manth[i]+'[яа])',interval_size[0][2])
                    if len(_manth)>0:
                        date_now = datetime.today()
                        date = datetime(date_now.year, i+1, int(interval_size[0][1]))
                        break
            else:
                date = datetime.strptime("1/1/10 00:00", "%d/%m/%y %H:%M")
       
        return date

