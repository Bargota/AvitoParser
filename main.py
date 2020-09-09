import BaseParser
import avito
import domofond
import Cian
import WorkLists
import time
import sys
#sys.path.insert(0, 'C:\\v.orlov\\Programm\\python\\AvitoParser\\YearOfConstruction')
sys.path.insert(0, 'D:\\v.orlov\\Programm\\python\\2\\AvitoParser\\YearOfConstruction')

from WorkLists import Settings

TEST_ONLY_LAST_PAGE=2
TEST_ONLY_TWO_PAGE=1
TEST_ALL_PAGE=0



start_time = time.time()
#TEST=TEST_ONLY_TWO_PAGE
TEST=TEST_ALL_PAGE
#TEST=TEST_ONLY_LAST_PAGE

my_set = Settings()
if TEST==TEST_ALL_PAGE or TEST==TEST_ONLY_LAST_PAGE:    
    my_set,good_read_flag = WorkLists.ReadSettingsAll('Настройки!B2:D7','Настройки!G2:G','Настройки!H2:H','Настройки!K2:K4')
else:
    #list=['https://www.avito.ru/kazan/kvartiry/prodam-ASgBAgICAUSSA8YQ?pmax=2000000&pmin=1000000']
    my_set.url_avito='https://www.avito.ru/kazan/kvartiry/prodam-ASgBAgICAUSSA8YQ?pmax=2100000&pmin=1500000'
    my_set.url_domofond='https://www.domofond.ru/prodazha-kvartiry-kazan-c1330?PriceFrom=1300000&PriceTo=2000000'
    my_set.url_cian='https://kazan.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&maxprice=2000000&minprice=1300000&offer_type=flat&quality=1&region=4777'
    good_read_flag=True

if good_read_flag:
   

    list_d=[]
    try:
        #my_d=domofond.domofondparser('https://www.domofond.ru/prodazha-nedvizhimosti/search?metroids=289%2c292%2c293%2c290%2c291&propertytypedescription=kvartiry&pricefrom=2000000&priceto=3200000&rooms=one%2ctwo&sortorder=pricepersquaremeterlow&distancefrommetro=upto3000m')
        my_d=domofond.DomofondParser(my_set.url_domofond)
        list_d = my_d.GetData(TEST)
        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        print('error: Domofond not parce')
    list_a=[]
    try:
        #my_a=avito.AvitoParser('https://www.avito.ru/kazan/kvartiry/prodam-ASgBAgICAUSSA8YQ?pmax=2100000&pmin=1500000&p=20')
        my_a=avito.AvitoParser(my_set.url_avito)
        list_a=my_a.GetData(TEST)
        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        print('Error: Avito not parce')

    list_c=[]
    #try:
    #    #my_c = Cian.Cian('https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&in_polygon%5B1%5D=49.084_55.7932%2C49.0929_55.7888%2C49.1002_55.784%2C49.1067_55.7791%2C49.1139_55.7747%2C49.1201_55.7698%2C49.1297_55.7675%2C49.1407_55.7658%2C49.1468_55.7609%2C49.152_55.7559%2C49.162_55.754%2C49.1726_55.7553%2C49.1826_55.7582%2C49.1901_55.7623%2C49.198_55.7665%2C49.2032_55.7716%2C49.2141_55.7735%2C49.2248_55.7737%2C49.2347_55.7753%2C49.2358_55.7811%2C49.2265_55.7849%2C49.2159_55.7851%2C49.2052_55.7845%2C49.1942_55.7849%2C49.1839_55.7865%2C49.175_55.7898%2C49.1692_55.795%2C49.162_55.7998%2C49.1537_55.8037%2C49.1451_55.807%2C49.1345_55.8072%2C49.1238_55.8064%2C49.1129_55.8054%2C49.1026_55.8043%2C49.106_55.8099%2C49.1039_55.8159%2C49.1015_55.8217%2C49.0954_55.8267%2C49.0868_55.83%2C49.0772_55.8275%2C49.0761_55.8217%2C49.0844_55.8174%2C49.0909_55.8128%2C49.0957_55.8076%2C49.094_55.8018%2C49.0885_55.7967&maxprice=3200000&minprice=2000000&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&quality=1&room1=1&room2=1&sort=price_square_order')
    #    my_c = Cian.Cian(my_set.url_cian)
    #    list_c = my_c.GetData(TEST)
    #    print("--- %s seconds ---" % (time.time() - start_time))
    #except:
    #    print('Error: Cian not parce')

    union_list = list_d+list_c+list_a    
    union_list=my_d._SortRepeat(union_list)


    #union_list = list_c+list_d
    #sort_list = WorkLists.SortListByAddress(union_list,my_set.bad_streets,my_set.good_streets)
    #sort_list=WorkLists.SortList(sort_list,my_set.list_dict_param)

    sort_list = WorkLists.SortListByAddress(union_list,my_set.bad_streets,my_set.good_streets)
    print('Сортировка по адресу. Количество до/после')
    print(str(len(union_list))+'/'+str(len(sort_list)))
    sort_list=WorkLists.SortList(sort_list,my_set.list_dict_param)

    WorkLists.import_Google_Sheet_all_data(sort_list)
    print('domofond adds count '+str(len(list_d)))
    print('avito adds count '+str(len(list_a)))
    print('Cian adds count '+str(len(list_c)))
    print("--- %s seconds ---" % (time.time() - start_time))


