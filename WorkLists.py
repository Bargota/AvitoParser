#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GoogleSheets


class Settings():
    def __init__(self):
        self.list_params=[]
        self.list_dict_param=[]
        self.good_streets=[]
        self.bad_streets=[]
        self.url_avito=''
        self.url_domofond=''
        self.url_cian=''


def ReadSettingsAll(range_param,range_good,range_bad,range_url):
    print('Read settings')
    flag_good_read=1
    
    try:
        my_GS_settings=GoogleSheets.myGoogleSheet()

        my_settings = Settings()

        my_settings.list_params=my_GS_settings.ReadData(range_param)
        my_settings.good_streets=List2List( my_GS_settings.ReadData(range_good))
        my_settings.bad_streets=List2List( my_GS_settings.ReadData(range_bad))
        urls=my_GS_settings.ReadData(range_url)
        my_settings.url_avito=urls[0]
        my_settings.url_domofond=urls[1]
        my_settings.url_cian=urls[2]
        
        my_settings.list_dict_param= ReadSettingsParam(my_settings.list_params)
        if flag_good_read:
           print('Reading settings success')
    except:
        flag_good_read=0
        print('Can\'t read settings')
    return my_settings, flag_good_read

def ReadSettingsParam(list_params):
    list_dict_param=[]
    for i in list_params:
            if i[0]!='area':
                i[1]=int(i[1].replace('\xa0',''))
                i[2]=int(i[2].replace('\xa0',''))
            else:
                i[1]=float(i[1].replace('\xa0',''))
                i[2]=float(i[2].replace('\xa0',''))

            param_dict={'param':i[0],'min':i[1],'max':i[2]}
            list_dict_param.append(param_dict)
    return list_dict_param

    


def ReadSettingsStreetsName(good_street,bad_street):
    print('Reading streets success')

def List2List(list):
    simple_list=[]
    for i in list:
        simple_list.append(i[0])
    return simple_list





def SortListByAddress(list,bad_list,good_list):
    #bad_list=['минская','авиастроительный','шигалеево',]
    #good_list = [
    #               #'ул',
    #             'толбухина','гвардейская',
    #             'седова','шуртыгина',
    #             'сахарова','стрелков',
    #             'даурская','такташ',
    #             'отрадная','курчатова',
    #             'гастело','товарищеская',
    #             'лумумбы',
    #             'кутуя','победы'
    #             'мавлютова','камала',
    #             'четаева','касимовых'
    #             ]
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

def SortListByArea(list,boarder_area=32):
    end_list=[]
    for i in list:
        if i['area']>boarder_area:
            end_list.append(i)
    return end_list

def SortListByFloors(list,boarder_floor=15):
    end_list=[]
    for i in list:
        if i['floors']>boarder_floor:
            end_list.append(i)
    return end_list

def SortListByParam(list,param_str,min_boarder, max_boarder):
    end_list=[]
    for i in list:
        if i[param_str]>min_boarder and i[param_str]<max_boarder:
            end_list.append(i)
    return end_list

#def SortList(list):
#	list1=SortListByParam(list,'area',30,1000)
#	list2=SortListByParam(list1,'floors',0,150)
#	list3=SortListByParam(list2,'price',2000000,3200000)
#	list4=SortListByParam(list3,'price_m2',0,90000)
#	print(str(len(list))+' '+str(len(list1))+' '+str(len(list2))+' '+str(len(list3))+' '+str(len(list4)))
#	#print(str(len(list))+' '+str(len(list1))+' '+str(len(list3))+' '+str(len(list4)))
#	return list4

def SortList(list,list_dict_param):
    list_for_log =[]
    list_for_log.append(len(list))
    for i in list_dict_param:
        list1=[]
        list1 = SortListByParam(list,i['param'],i['min'],i['max'])
        list_for_log.append(len(list1))
        list=list1

    
    for i in list_for_log:
        print(str(i),end=' ')
    
    
    return list



def import_Google_Sheet_all_data(list):
    all_data=[]
    if len(list)!=0:
        for i in list:
            i['title'] =  i['title'].replace('м²','м2')
            #i['price_m2'] =  i['price_m2'].replace('??','?2')
            i['address'] =  i['address'].replace('?','-')
            row_list=[
                       i['title'],
                       i['price'],
                       i['price_m2'],
                       str(i['area']),
                       i['year'],
                       i['found_addres'],
                       i['address'],
                       i['urlad'],
                       str(i['floors'])
                       #data['type_house'],
                       #data['date_ad']
                       ]
            all_data.append(row_list)
        gs = GoogleSheets.myGoogleSheet()
        #gs.AppendRow('????1!A1',all_data)
        gs.AddData('Смотреть тут!A1',all_data)
    else:
        print('Итоговый список пуст')

