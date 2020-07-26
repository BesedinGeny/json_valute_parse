import json 
import requests
import pymysql
import datetime
from pymysql.cursors import DictCursor
import pylab
import matplotlib.dates

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

colors = ["b-", "g-", "r-", "c-"]

axes = pylab.subplot(1, 1, 1)
axes.xaxis.set_major_formatter (matplotlib.dates.DateFormatter("%m-%d"))

#Работа с бд с помощью курсора
with connection.cursor() as cursor:
    i = 0
    for val in valutes:
        query = "SELECT date,value FROM vals WHERE name = \'" + val + "\'"
        #query = "SELECT * FROM vals"
        cursor.execute(query)
        data = cursor.fetchall()
        
        dates = []
        values = []
        for curData in data:
            dates.append(curData["date"])
            values.append(curData["value"])
        xdata_float = matplotlib.dates.date2num (dates)
        axes.plot(dates, values, colors[i], label=val)
        axes.legend()
        pylab.plot_date (xdata_float, values, fmt=colors[i])
        i+=1

    pylab.grid()
    pylab.show()
        
connection.close()