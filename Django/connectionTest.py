# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 23:57:55 2020

@author: stvyh
"""
import sqlalchemy
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
#"mssql+pyodbc://@DESKTOP-F9VFK3C/SMS?driver=SQL+Server+Native+Client+11.0?trusted_connection=yes")
data ={}
data['first']= 'line0'

conn = pyodbc.connect('Driver={SQL Server};'
                  'Server=DESKTOP-F9VFK3C;'
                  'Database=TEST;'
                  'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('SELECT * FROM airports')
data['result'] = result = cursor.fetchall()

print(data)

for row in result:
    print(row)
    
print('======================')
print(dict(result))