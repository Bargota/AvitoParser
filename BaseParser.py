import requests
import re
import sys
sys.path.insert(0, 'P:\\Programm\\Pyton\\AvitoParser\\YearOfConstruction\\')
from main_for_year import FoundYearFromAddres
from GoogleSheets import myGoogleSheet


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
            ads = soup.find(key,class_=class_).find_all(key_all,class_=class_all)
        except:
            ads = []
        return ads

    def _FindArea(self,title_str):
        if title_str!="":
            area = re.findall(r'(\d{2}.?\d?) м²',title_str)
            float_area  = float(area[0])
            return float_area
        return 0

    def _FindPriceM2(self,price,area):
        if area!=0:
            return round(price/area,0)
        return 0

    def _FindFloors(self,title_str):
        if title_str!="":
            floor = re.findall(r'/(\d{1,2}) эт.',title_str)
            floors  = int(floor[0])
            return floors
        return 0

    def _FindYear(self,addres_str):
        my_found_year_from_addres=FoundYearFromAddres()
        path_file_streets='P:\\Programm\\Pyton\\AvitoParser\\YearOfConstruction\\'
        name_file_streets='streets_list.txt'
        year = my_found_year_from_addres.FindYearOfConstruction(addres_str,path_file_streets+name_file_streets,self.list_addres_and_year)
        return year,my_found_year_from_addres.street_name +' '+my_found_year_from_addres.house_number