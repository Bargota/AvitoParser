#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

class FindAddres:
	def __init__(self):
		self.street_name = ''
		self.place_in_string = 0
		self.house_number = ''



def find_addres(path_address,path_street):
	all_streets = open(path_street,'r')
	address = open(path_address,'r')

	
	count1=0
	count2=0
	count3=0
	list=[]
	for addres in address:
		addres=re.sub(r'\s+',' ',addres)
		addres=addres.lower().strip()
		count1+=1		
		my_addres = FindAddres()
		my_addres.street_name, my_addres.place_in_string=find_regular_street(addres,path_street)
		my_addres.house_number=find_regular_house(addres,my_addres.place_in_string)
		
		list.append({'street':my_addres.street_name,'house':my_addres.house_number})
		#if count1%20==0:
		#	print(str(my_addres.place_in_string)+' '+my_addres.street_name+' '+addres[my_addres.place_in_string:])

		#print(str(count1)+' '+my_addres.street_name+' '+addres)
	return list


def find_regular_street(addres,path_street):
	all_streets = open(path_street,'r')
	list_streets=[]
	flag_uncertainty=0
	flag_not_found=1
	for street_name in all_streets:
		list_streets.append(street_name)

	tmp=re.findall(r',? ?\bул(?:иц[ае])?[ \.][^,]{3,},?', addres)
	tmp2=re.findall(r',?[^,]+ \bул(?:иц[ае])?,?', addres)
	if len(tmp)==0 and len(tmp2)==0:
		previously_found_street=addres			
	else:			
		if len(tmp2)==0:
			previously_found_street = StreetNameRemoveExcess(tmp[0])
				
		if len(tmp)==0:
			previously_found_street = StreetNameRemoveExcess(tmp2[0])
	if len(tmp)!=0 and len(tmp2)!=0:
		previously_found_street=tmp[0]
		flag_uncertainty=1
				
	for street in list_streets:
			if previously_found_street.find(street.strip().lower())!=-1:					
				found_street=street.strip()
				flag_not_found=0
				break

	if flag_uncertainty:
		if flag_not_found:
			for street in list_streets:
				if tmp2[0].find(street.strip().lower())!=-1:					
						found_street=street.strip()
						break

	place = addres.find(found_street.lower())
	if place!=-1:
		place+=len(found_street)
		
	if place>len(addres) or place==-1:
		print('Название улицы распозналось не корректно, суммарная длина больше длины адреса')
		place=0
	
	return found_street,place

def find_regular_house(addres,place):
	"""Search for the number of house in addres"""
		
	
	
		
	addres=re.sub(r'\s+',' ',addres)
	addres=addres.lower().strip()
	

	regular = re.compile(r',? д?(?:ом)? ?\d{1,4}/?\\?\w{0,4},?')
	tmp=regular.search(addres,place)
	#tmp2=re.findall(r',?[^,]+ ул\w{3},?', addres)
	if tmp!=None:
		found_house = re.sub(r', ?','',addres[tmp.regs[0][0]:tmp.regs[0][1]])
		found_house = re.sub(r' ?д?(?:ом)?','',found_house)
	else:
		print('номер дома не найден')
		found_house=str(0)

	return found_house
	#if len(tmp)!=0 :
	#	previously_found_house=tmp		
	#print (str(count1)+' '+previously_found_house)		
			

	
	

def StreetNameRemoveExcess(name_street):
	'''Delete from street name word 'street' '''
	
	name_street = re.sub(r'[ \.,]\bул(?:иц[ае])?[ \.,]','',name_street)
	
	name_street = re.sub(r', ?','',name_street)
	
	return name_street




		




#path_file = 'C:\\v.orlov\\Programm\\python\\AvitoParser\\YearOfConstruction\\address.txt'
#path_all_streets='C:\\v.orlov\\Programm\\python\\AvitoParser\\YearOfConstruction\\streets_list.txt'
#file = open(path_file,'r')
#all_streets = open(path_all_streets,'r')

main_path=sys.path[0]
file_name_address = 'address.txt'
file_name_streets='streets_list.txt'
#address = open(main_path+'\\'+file_name_address,'r')
#streets = open(main_path+'\\'+file_name_streets,'r')


#find_regular_word(path_file)
#find_street_name_from_file(main_path+'\\'+file_name_address,main_path+'\\'+file_name_streets)

#find_regular_street(main_path+'\\'+file_name_address,main_path+'\\'+file_name_streets)
#find_regular_house(main_path+'\\'+file_name_address)

find_addres(main_path+'\\'+file_name_address,main_path+'\\'+file_name_streets)
print('finish')
input()

#---------------------------------------------------------------------------------------------------

def find_regular_word(file):
	"""Search for the word 'street' in addres"""

	count = 0
	count1 = 0
	count2 = 0
	for line in file:
		#line=line.replace(" ",' ')
		#line=line.replace(" ",' ')
		line=re.sub(r'\s+', ' ', line)
		street = re.findall(r'ул\w* (\w+)',line)
	
		if len(street) == 0:
			count+=1
			street = re.findall(r'(\w+) ул\w*',line)
			if len(street) == 0:
				count1+=1
		else:
			count2+=1
		
		print(street)
	print(str(count2))
	print(str(count))
	print(str(count1))

def find_street_name_from_file(path_address,path_all_streets_file):
	all_streets = open(path_all_streets_file,'r')
	address = open(path_address,'r')
	count_all =0
	count_not_found=0
	count_overlap2=0
	count_tatar =0
	list_streets=[]
	list_abbreviation=[' ул',' пер',' пр']
	for street_name in all_streets:
		list_streets.append(street_name)
	ld=[]
	count_found=0
	for addres in address:
		#addres=addres.replace('Республика Татарстан','')
		#addres=addres.replace('Татарстан Республика','')
		#addres=addres.replace('Казань','')
		addres=re.sub(r'\s+', ' ', addres)
		count_overlap=0
		count_street=0
		count_all+=1
		count1=0
		list=addres.split(',')
		for item in list:
			for i in list_abbreviation:
				flag=0
				
				if item.find(i)!=-1:
					
					flag=1
					for street in list_streets:						
						street=street.strip()
						
						if item.lower().find(street.lower())!=-1:
							
							count_not_found-=1
							count_found+=1
							count_overlap+=1
							#print(str(count_overlap)+' '+street.strip()+' '+addres.strip())
							if count_overlap==1:	
								tmp=street
							if count_overlap==2:								
								if street!=tmp:
									count_overlap2+=1
									d={'s1':street,'s2':tmp,'add':addres}
									ld.append(d)
						else:
							if count_street==0:								
								count_not_found+=1
							count_street+=1
				if flag==0:
					count1+=1
					print(str(count_not_found)+' '+  addres.strip())
																		
		
		
	print ('1 '+str(count1))
	#for i in ld:
	#	print(i['s1']+' '+i['s2']+ ' '+i['add'].strip())
							
			
			#street=street.strip()
			##if addres.find(street)!=-1:
			#if addres.find('ул '+street)!=-1 or addres.find('ул. '+street)!=-1 or addres.find(street+' ул')!=-1 or addres.find(street+' ул.')!=-1 or addres.find(street+' улица')!=-1 or addres.find('улица '+street)!=-1:
			#	#print(str(count_overlap)+' '+street+' '+addres.strip())
			#	count_overlap+=1
			#	count_not_found-=1
			#	if count_overlap==1:
			#		count_found+=1
			#	if count_overlap==2:
			#		count_overlap2+=1
			#		if street=='Татарстан':
			#			count_tatar+=1	
			#else:
			#	if count_street==0:
			#		#print(addres.strip())	
			#		count_not_found+=1
			#		pass				
			#	count_street+=1



					
	print('all '+str(count_all))
	print('found '+str(count_found))
	print('repeat '+str(count_overlap2))
	print('not found '+str(count_not_found))

