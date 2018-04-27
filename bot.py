# -*- coding: utf-8 -*-

import telebot
from lxml import etree
import requests
import urllib3  
import lxml.html
import re

token = '364176271:AAFnWXuMVo_ekKts7AMiCCqM22fkv2zQW_Q'

bot = telebot.TeleBot(token)

# Всего 34 группы
groups = [
    '1РА-17-1уп',
    '1РА-17-2',
    '1РЭТ-17-1',
    '1КСК-17-1',
    '1ОТЗИ-17-1',
    '1ИСИП-17-1',
    '1ИСИП-17-2к',
    '1ПКС-17-1к',
    '1РЭТ-17-2с',
    '1ПКС-17-2с',
    '2РА-16-1',
    '2РА-16-2',
    '2РЭТ-16-1',
    '2ПКС-16-1',
    '2ПКС-16-2',
    '2КСК-16-1',
    '2ИС-16-1',
    '2РЭТ-16-2с',
    '2ИС-16-2с',
    '3РА-15-1',
    '3РА-15-2',
    '3РЭТ-15-1',
    '3КСК-15-1',
    '3ПКС-15-1',
    '3ИС-15-1',
    '3РЭТ-15-2с',
    '3ИС-15-2с',
    '4РА-14-1',
    '4РА-14-2',
    '4РЭТ-14-1',
    '4КСК-14-1',
    '4КСК-14-2',
    '4ОТЗИ-14-1',
    '5РА-13-1уп'
]

def parse(groupname):
    #будущий ID нужной группы
    groupID = None
    #поиск ID
    for i in range(len(groups)):
        if groupname.lower() == groups[i].lower():
            groupID = i    

    #Проверка ввода. Программа закрывается, если название не верно
    if groupID is None:
        return ('Ошибка ввода. Группа не найдена.')
         

    session = requests.Session()
    URL = 'https://nntc.nnov.ru/sites/default/files/sched/zameny.html'

    all_html = session.get(URL)
    all_html.encoding = 'utf-8'
    all_html = all_html.text

    # Парсим имеющиеся названия дней недели
    tree = lxml.html.fromstring(all_html) 
    days = tree.xpath('//center/a/text()')



    #узнаем кол-во таблиц для парсинга(1 или 2)
    if(len(days) == 3):
        myLen = 2
    elif(len(days) == 2):
        myLen = 1 

    # Массив указателей на символ откуда парсить таблицы
    tablesp = []      

    # записываем номер символа в массив
    for i in range(myLen):
        tablesp.insert(i,all_html.find('<A NAME="table' + str(i+1) + '">')) 

    # массив таблиц    
    tables = []

    

    #len(days) == 3
    #записываем нужные  таблицы в массив. от <table до </table> включительно
    for i in range(myLen):
        if (i + 1 != (len(days)-1)):
            table1 = all_html[tablesp[i]:tablesp[i+1]]
            table1 = table1[table1.find('<table'):table1.find('<!--')]
            tables.insert(i,table1)
        else:
            table1 = all_html[tablesp[i]:]
            table1 = table1[table1.find('<table'):table1.find('<!--')]
            tables.insert(i,table1)


    # массив подтаблиц каждый группы
    groupsTable = [[],[]]
    # Массив указателей на символ откуда парсить подтаблицы
    gTabgesp = [[],[]]
    for i in range(myLen):
        for j in range(len(groups)):
            gTabgesp[i].insert(j,tables[i].find(groups[j])) 

        for c in range(len(groups)):
            if (c != (len(groups)-1)):
                gtable = tables[i][gTabgesp[i][c]:gTabgesp[i][c+1]]
                groupsTable[i].insert(c,gtable)
            else:
                gtable = tables[i][gTabgesp[i][c]:]
                groupsTable[i].insert(c,gtable)


        return (days[i+1] + '\n' + re.sub(r'\<[^>]*\>', '', groupsTable[i][groupID]))





@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе

	bot.send_message(message.chat.id, parse(message.text))





if __name__ == '__main__':
	bot.polling(none_stop=True)

