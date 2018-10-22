#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def find_regular(file):
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

def find_street_name_from_file(address,path_all_streets_file):
    all_streets = open(path_all_streets_file,'r')
    address=address.replace('Республика Татарстан','')
    address=address.replace('Татарстан Республика','')
    address=address.replace('Казань','')
    count =0
    count1=0
    count2=0
    for street_name in all_streets:
        street_name=street_name.strip()
        if address.find(street_name)!=-1:
            print(str(count)+' '+street_name+' '+address.strip())
            count+=1
        
        




path_file = 'C:\\v.orlov\\Programm\\python\\AvitoParser\\YearOfConstruction\\address.txt'
path_all_streets='C:\\v.orlov\\Programm\\python\\AvitoParser\\YearOfConstruction\\streets_list.txt'

file = open(path_file,'r')
all_streets = open(path_all_streets,'r')

#find_regular(path_file)
for line in file:
    find_street_name_from_file(line,path_all_streets)

input()

