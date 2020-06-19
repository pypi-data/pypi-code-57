import win32com.client

AP_name = 'CAGE CODE - 70628'
BWT_name = 'CAGE CODE - K2692'
names = [AP_name, BWT_name]

CATIA = win32com.client.Dispatch('CATIA.Application')

active_document = CATIA.ActiveDocument.Part

body = active_document.Bodies

body.Add()
body.Name = AP_name



# for body in body:
#     print(body.Name)

body.Add()
body.Name = BWT_name