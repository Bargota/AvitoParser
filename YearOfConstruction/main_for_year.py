#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys


sys.path.insert(0, 'C:\\v.orlov\\Programm\\python\\AvitoParser')
sys.path.insert(0, 'C:\\v.orlov\\Programm\\python\\AvitoParser\\YearOfConstruction')
from GoogleSheets import myGoogleSheet



class FoundYearFromAddres:
    def __init__(self):
        self.street_name = ''
        self._place_in_string = 0
        self.house_number = ''
        self.year_of_construction='0'




    def FindYearOfConstruction(self,addres,path_street,list_addres_and_year):
        all_streets = open(path_street,'r')
    
        
    
        addres = re.sub(r'\s+',' ',addres)
        addres = addres.lower().strip()
    
        self.street_name, self._place_in_string = self._FindRegularStreet(addres,path_street)
        if self.street_name!='':
            self.house_number = self._FindRegularHouse(addres,self._place_in_string)
            if self.house_number!=0:
                self._YearFromAddres(list_addres_and_year)
        
    
        return  self.year_of_construction

    def _YearFromAddres(self,list_addres_and_year):
        try:
            for i in list_addres_and_year:
                tmp_addres = i[0].lower()
                if tmp_addres.find(self.street_name.lower())!=-1:
                    if len(re.findall(r'\b'+self.house_number.lower(),tmp_addres))!=0:
                    #if tmp_addres.find(self.house_number.lower())!=-1:
                        self.year_of_construction=i[2]
                        break
        except:
            print('Error: при поиске года постройки по адресу из списка')
            pass





    def _FindRegularStreet(self,addres,path_street):
        all_streets = open(path_street,'r')
        list_streets = []
        flag_uncertainty = 0
        flag_not_found = 1
        for street_name in all_streets:
            list_streets.append(street_name)

        tmp = re.findall(r',? ?\bул(?:иц[ае])?[ \.][^,]{3,},?', addres)
        tmp2 = re.findall(r',?[^,]+ \bул(?:иц[ае])?,?', addres)
        found_street=''
        if len(tmp) == 0 and len(tmp2) == 0:
            previously_found_street = addres			
        else:			
            if len(tmp2) == 0:
                previously_found_street = self._StreetNameRemoveExcess(tmp[0])
                
            if len(tmp) == 0:
                previously_found_street = self._StreetNameRemoveExcess(tmp2[0])
        if len(tmp) != 0 and len(tmp2) != 0:
            previously_found_street = tmp[0]
            flag_uncertainty = 1
                
        for street in list_streets:
                if previously_found_street.find(street.strip().lower()) != -1:					
                    found_street = street.strip()
                    flag_not_found = 0
                    break

        if flag_uncertainty:
            if flag_not_found:
                for street in list_streets:
                    if tmp2[0].find(street.strip().lower()) != -1:					
                            found_street = street.strip()
                            break
        if found_street!='':
            place = addres.find(found_street.lower())
            if place != -1:
                place+=len(found_street)
        
            if place > len(addres) or place == -1:
                print('Название улицы распозналось не корректно, суммарная длина больше длины адреса')
                place = 0
        else:
            place=0
            print(previously_found_street+' Не найдена улица в общем списке')
    
        return found_street,place

    def _FindRegularHouse(self,addres,place):
        """Search for the number of house in addres"""
        
    
    
        
        addres = re.sub(r'\s+',' ',addres)
        addres = addres.lower().strip()
    

        regular = re.compile(r',? д?(?:ом)? ?\d{1,4}/?\\?\w{0,4},?')
        tmp = regular.search(addres,place)
        #tmp2=re.findall(r',?[^,]+ ул\w{3},?', addres)
        if tmp != None:
            found_house = re.sub(r', ?','',addres[tmp.regs[0][0]:tmp.regs[0][1]])
            found_house = re.sub(r' ?д?(?:ом)?','',found_house)
        else:
            #print('номер дома не найден')
            found_house = str(0)

        return found_house
        #if len(tmp)!=0 :
        #	previously_found_house=tmp		
        #print (str(count1)+' '+previously_found_house)		
            

    
    

    def _StreetNameRemoveExcess(self,name_street):
        '''Delete from street name word 'street' '''
    
        name_street = re.sub(r'[ \.,]\bул(?:иц[ае])?[ \.,]','',name_street)
    
        name_street = re.sub(r', ?','',name_street)
    
        return name_street



def _FindAddres(path_address,path_street):
    all_streets = open(path_street,'r')
    address = open(path_address,'r')
    #чтение данных из гугл таблицы о адресе и годе постройки
    GS_settings_year = myGoogleSheet()
    list_addres_and_year = GS_settings_year.ReadData('mingkh.ru!B2:E6000')
    
    count1 = 0
    count2 = 0
    count3 = 0
    list = []
    for addres in address:
        addres = re.sub(r'\s+',' ',addres)
        addres = addres.lower().strip()
        count1+=1		
        my_addres = FoundYearFromAddres()
        my_addres.street_name, my_addres.place_in_string = find_regular_street(addres,path_street)
        my_addres.house_number = find_regular_house(addres,my_addres.place_in_string)

        YearFromAddres(my_addres,list_addres_and_year)
        
        list.append({'street':my_addres.street_name,'house':my_addres.house_number,'year':my_addres.year_of_construction})
        #if count1%20==0:
        #	print(str(my_addres.place_in_string)+' '+my_addres.street_name+'
        #	'+addres[my_addres.place_in_string:])

        #print(str(count1)+' '+my_addres.street_name+' '+addres)
    return list

        



#---------------------------------------------------------------------------------------------------

#main_path=sys.path[0]
#file_name_address = 'address.txt'
#file_name_streets = 'streets_list.txt'

#list =find_addres(main_path + '\\' + file_name_address,main_path + '\\' + file_name_streets)

#for i in list:
#    print(i['street']+' '+
#          i['house']+' '+
#          str(i['year'])
#          )



#print('finish')
#input()



