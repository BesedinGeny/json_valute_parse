import json 
import requests
import pymysql
import datetime
from pymysql.cursors import DictCursor

#Вход в бд, позже надо сделать пароль и логин из файла и файл бы спрятать
connection = pymysql.connect(
    host='localhost',
    user='user',
    password='User12345!',
    db='valutes',
    charset='utf8mb4',
    cursorclass=DictCursor
)

valutes = ["USD", "EUR", "CNY", "JPY"]


#Получаем стартовый юрл
url = "https://www.cbr-xml-daily.ru/daily_json.js"
https = "https:"
curURL = url

#берем данные с сайта и работаем с ними как с json 
response = requests.get(url)
info = json.loads(response.text)


#Получаем дату окончания месяца
curDate = info["Date"]
curDate = curDate[:10].replace("-", "")
curDate = datetime.datetime.strptime(curDate, '%Y%m%d').date()
lastDate = curDate - datetime.timedelta(days=30)


#получаем новую ссылку по которой будем переходить
prevUrl = info["PreviousURL"]
prevUrl = prevUrl[2:]



#Работа с бд с помощью курсора
with connection.cursor() as cursor:
    while curDate > lastDate:
        
        #Обрабатываю текущий день
        response = requests.get(curURL)
        info = json.loads(response.text)

        #работа с данными
        for valute in valutes:
            
            val = float(info["Valute"][valute]["Value"])
            query = 'INSERT INTO vals(name, date, value) VALUES (%s, %s, %s)'
            print("INSERTING " + valute + " with value " + str(val / float(info["Valute"][valute]["Nominal"])))
            cursor.execute(query, (valute, curDate, val / float(info["Valute"][valute]["Nominal"])))
            connection.commit()

        # переход к предыдущему дню
        prevUrl = info["PreviousURL"]  
        prevUrl = https + prevUrl
        curURL = prevUrl

        response1 = requests.get(str(prevUrl))
        
        info = json.loads(response1.text)
        curDate = info["Date"]
        curDate = curDate[:10].replace("-", "")
        curDate = datetime.datetime.strptime(curDate, '%Y%m%d').date()
    
connection.close()
