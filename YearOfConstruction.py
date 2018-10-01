import transliterate
import requests
from bs4 import BeautifulSoup
import re #импорт модуля регулярных выражений
import csv
from avito import GetHTMLText 


def Txt2ListDictionary(file):
    dictionary={}
    list=[]
    with open(file) as file_read:
        for line in file_read:
            line=line.strip()
            if line!='':
                string = line.split(',')
                dictionary={'street':string[0],
                            'house':string[1].strip()}
                list.append(dictionary)            
    return list

def TransliterateNameStreet(street_name_kirilica_str):
    latinica = transliterate.translit(street_name_kirilica_str, reversed=True)
    return  latinica

def YearOfConstructionGinfo(street_name_str,house_number_str):
    url_base = "http://kazan.ginfo.ru//ulicy//ulica_"
    ulica_latinica = TransliterateNameStreet(street_name_str)
    url = url_base+ulica_latinica+"//"+house_number_str+"/"
    html = GetHTMLText(url)
    soup = BeautifulSoup(html)
    try:
        info= soup.find('table',class_='dom_info').find_all('tr')
        year_of_construction = info[1].find_all('td')[1].text
    except:
        year_of_construction=''
    
    return year_of_construction

def YearOfConstructionDomMinGKH(url):
    html = GetHTMLText(url)
    soup = BeautifulSoup(html)
    try:
        info= soup.find('dl',class_='dl-horizontal')
        year_of_construction = info.find_all('dd')[1].text
    except:
        year_of_construction=''
    
    return year_of_construction


def YearOfConstructionGinfoGoogleUrl(url):
    html = GetHTMLText(url)
    soup = BeautifulSoup(html)
    try:
        info= soup.find('table',class_='dom_info').find_all('tr')
        year_of_construction = info[1].find_all('td')[1].text
    except:
        year_of_construction=''
    
    return year_of_construction


def WriteLineTxt(file,street_str,house_str,year_str,url):
    f = open(file, "a")
    f.write(street_str+','+house_str+','+year_str+','+url+'\n')

    f.close()

def GoogleRequest(street,house):
    #url_google = 'https://www.google.ru/search?q=ginfo+'+street+'+'+house+ '&ie=utf-8&oe=utf-8'
    url_google = 'https://www.google.ru/search?q=dom.mingkh+казань+'+street+'+'+house+ '&ie=utf-8&oe=utf-8'
    html_google = GetHTMLText(url_google)
    soup_google = BeautifulSoup(html_google)
    try:
        ginfo_url1='http://'+ soup_google.find_all('h3',class_='r')[0].find('a').get('href')
        ginfo_url = re.findall(r'(http://dom.mingkh.ru/tatarstan/kazan/[0-9]{0,15})&.+',ginfo_url1)[0]
    except:
        ginfo_url=''
    return ginfo_url




#file_read_txt = 'C:\v.orlov\Programm\python\AvitoParser\read.txt'
file_read_txt = 'read.txt'
file_write_txt = 'write.txt'
list_dictionary = Txt2ListDictionary(file_read_txt)
i=1
for item in list_dictionary:
    address_url=GoogleRequest(item.get('street'),item.get('house'))
    if address_url!='':
        year = YearOfConstructionDomMinGKH(address_url)
    else:
        year=''
    WriteLineTxt(file_write_txt,item.get('street'),item.get('house'),year,address_url)
    print(str(i)+','+item.get('street')+','+item.get('house')+','+year+'    '+address_url)
    i=i+1




