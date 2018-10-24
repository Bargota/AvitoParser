#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

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

def find_regular_street(path_address,path_street):
	all_streets = open(path_street,'r')
	address = open(path_address,'r')

	list_streets=[]
	for street_name in all_streets:
		list_streets.append(street_name)

	for addres in address:
		for addres in address:




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



input()

