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

#Работа с бд с помощью курсора
with connection.cursor() as cursor:
    query = "SELECT DISTINCT date FROM vals"
    cursor.execute(query)
    dates = cursor.fetchall()
    for curDate in dates:
        query = "SELECT name,value FROM vals WHERE date = \'" + str(curDate["date"]) + "\'" 
        cursor.execute(query)
        results = cursor.fetchall()
        for ires in results:
            for jres in results:
                if ires != jres:
                    query = 'INSERT INTO diffs(valute1, valute2, value) \
                        VALUES (%s, %s, %s)'
                    diffinition = float(ires["value"])/float(jres["value"])
                    print("INSERTING " + ires["name"] + " to " + jres["name"] + " is " + str(diffinition))
                    cursor.execute(query, (ires["name"], jres["name"], diffinition))
                    connection.commit()
        
connection.close()