import requests
from bs4 import BeautifulSoup
import re #импорт модул€ регул€рных выражений


import BaseParser


def GetHTMLText(url):
    try:
        r=requests.get(url)
    except:
        return ''
    return r.text

def GetTotalPages(html):
    
    total_page=''
    while total_page=='' or total_page=='..':
        soup = BeautifulSoup(html)
        tmp = soup.find('div', id='frontend-serp').find('ul',class_='_93444fe79c-list--35Suf').find_all('li', class_='_93444fe79c-list-item--2QgXB')[-1]
        total_page=tmp.text
        if total_page=='..':
            url='https://www.cian.ru'+tmp.find('a').get('href')
            try:
                r=requests.get(url)
                html = r.text
            except:
                total_page=10


        
    

    

    #total_pages = tmp_pages.split('=')[1]
    
    return total_page


url='https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&in_polygon%5B1%5D=49.084_55.7932%2C49.0929_55.7888%2C49.1002_55.784%2C49.1067_55.7791%2C49.1139_55.7747%2C49.1201_55.7698%2C49.1297_55.7675%2C49.1407_55.7658%2C49.1468_55.7609%2C49.152_55.7559%2C49.162_55.754%2C49.1726_55.7553%2C49.1826_55.7582%2C49.1901_55.7623%2C49.198_55.7665%2C49.2032_55.7716%2C49.2141_55.7735%2C49.2248_55.7737%2C49.2347_55.7753%2C49.2358_55.7811%2C49.2265_55.7849%2C49.2159_55.7851%2C49.2052_55.7845%2C49.1942_55.7849%2C49.1839_55.7865%2C49.175_55.7898%2C49.1692_55.795%2C49.162_55.7998%2C49.1537_55.8037%2C49.1451_55.807%2C49.1345_55.8072%2C49.1238_55.8064%2C49.1129_55.8054%2C49.1026_55.8043%2C49.106_55.8099%2C49.1039_55.8159%2C49.1015_55.8217%2C49.0954_55.8267%2C49.0868_55.83%2C49.0772_55.8275%2C49.0761_55.8217%2C49.0844_55.8174%2C49.0909_55.8128%2C49.0957_55.8076%2C49.094_55.8018%2C49.0885_55.7967&maxprice=3100000&minprice=2000000&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&quality=1&room1=1&room2=1&sort=price_square_order'
total_pages = GetTotalPages(GetHTMLText(url))		 

