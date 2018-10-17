#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GoogleSheets


def ConectLists(list1,list2):
	return list1+list2
	#if len(list1)>len(list2):
	#	for i in list2:
	#		list1.append(i)
	#	return list1
	#else:
	#	for i in list1:
	#		list2.append(i)
	#	return list2


def SortListByAddress(list):
	bad_list=['минская','авиастроительный','шигалеево',]
	good_list = [
                   'ул',
				 'толбухина','гвардейская',
				 'седова','шуртыгина',
				 'сахарова','стрелков',
				 'даурская','такташ',
				 'отрадная','курчатова',
				 'гастело','товарищеская',
				 'лумумбы',
				 'кутуя','победы'
                 'мавлютова','камала',
                 'четаева','касимовых'
                 ]
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

def SortList(list):
	list1=SortListByParam(list,'area',31.9,1000)
	list2=SortListByParam(list1,'floors',0,15)
	list3=SortListByParam(list2,'price',2000000,3100000)
	list4=SortListByParam(list3,'price_m2',70000,85000)
	print(str(len(list))+' '+str(len(list1))+' '+str(len(list2))+' '+str(len(list3))+' '+str(len(list4)))
	return list4

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

