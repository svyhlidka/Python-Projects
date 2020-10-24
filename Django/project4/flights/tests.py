from django.test import TestCase
import pyodbc

# Create your tests here.
conn = pyodbc.connect('Driver={SQL Server};'
                  'Server=DESKTOP-F9VFK3C;'
                  'Database=TEST;'
                  'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('SELECT * FROM flights')
result = cursor.fetchall()
print(result)