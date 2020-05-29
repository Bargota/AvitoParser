
import re
from datetime import datetime, date, time,timedelta

def WhatIntervel(reg_exp,interval_str,interval_num,how_many_day=0):
    interval=re.findall(r'('+reg_exp+')',interval_str)
    date=None
    if len(interval)>0:
        date = datetime.today() - timedelta(days=int(interval_num)*how_many_day)
    return date

def ParseDate(line):    
    word_back=re.findall(r'() назад',line)
    if len(word_back)>0:
        interval_size=re.findall(r'((\d{1,2}) ((недел[юи])|(де?н(ь|(ей)|я))|(час((ов)|а)?)|(минуту?)|(месяц(ев|а))|((года?)|(лет))))',line)
        if len(interval_size)>0:
            date=None
            if (date==None):
                date=WhatIntervel('(час((ов)|а)?)|(минуту?)',interval_size[0][2],interval_size[0][1],0)
            if (date==None):
                date=WhatIntervel('де?н(ь|(ей)|я)',interval_size[0][2],interval_size[0][1],1)
            if (date==None):
                date=WhatIntervel('недел[юи]',interval_size[0][2],interval_size[0][1],7)
            if (date==None):
                date=WhatIntervel('месяц(ев|а)',interval_size[0][2],interval_size[0][1],30)
            if (date==None):
                date=WhatIntervel('(года?)|(лет)',interval_size[0][2],interval_size[0][1],355)
        else:
            date = datetime.strptime("1/1/11 00:00", "%d/%m/%y %H:%M")
    else:
        list_manth=['январ',
              'феврал',
              'март',
              'апрел',
              'ма',
              'июн',
              'июл',
              'август',
              'сентябр',
              'октябр',
              'ноябр',
              'декабр'
              ]
        #interval_size=re.findall(r'((\d{1,2}) ([А-Яа-я]) )',line)
        interval_size=re.findall(r'((\d{1,2}) (\w{2,7}) )',line)
        if len(interval_size)>0:
            for i in range(len(list_manth)):
                _manth=re.findall(r'('+list_manth[i]+'[яа])',interval_size[0][2])
                if len(_manth)>0:
                    date_now = datetime.today()
                    date = datetime(date_now.year, i+1, int(interval_size[0][1]))
        else:
            date = datetime.strptime("1/1/10 00:00", "%d/%m/%y %H:%M")
       
    return date



def MainFindDate():
    FILE_NAME="date_example.txt"
    Fin = open (FILE_NAME, "r" )
    for line in Fin:
        ParseDate(line)


    Fin.close()

#MainFindDate()
print('1')
print('/n')
print('1')
