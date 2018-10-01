import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pyperclip


CREDENTIALS_FILE = 'AvitoParser-fa42c491fb6e.json'  # имя файла с закрытым ключом

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Сие есть название документа', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Сие есть название листа',
                               'gridProperties': {'rowCount': 8, 'columnCount': 5}}}]
}).execute()

#Доступ к фйлу через Google Drive API
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
shareRes = driveService.permissions().create(
    fileId = spreadsheet['spreadsheetId'],
    #body = {'type': 'user', 'role': 'writer', 'emailAddress': 'v.orlov.geo@gmail.com'}, 
    body={'type': 'anyone', 'role': 'reader'}, # доступ на чтение кому угодно
    fields = 'id'
).execute()

print(spreadsheet['spreadsheetId'])
pyperclip.copy(spreadsheet['spreadsheetId'])

results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet['spreadsheetId'], body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "Сие есть название листа!B2:C3",
         "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
         "values": [["This is B2", "This is C2"], ["This is B3", "This is C3"]]},

        {"range": "Сие есть название листа!D5:E6",
         "majorDimension": "COLUMNS",  # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
         "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]},
		 {"range": "Сие есть название листа!A1:A2",
         "majorDimension": "COLUMNS",  # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
         "values": [["=E6+12","123"]]}
    ]
}).execute()

print('123')

#results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet['spreadsheetId'], body = {
#    "valueInputOption": "USER_ENTERED",
#    "data": [
#        {"range": "Сие есть название листа!A1:A2",
#         "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
#         "values": [["This is B3", "This is C2"]]}]}).execute()

#request = service.spreadsheets().values().append(spreadsheetId='1Di7CgLURGb1rNLvyC8UVTgFZmh6LKBmFGtw9KlsHr6A',
#												 range="Сие есть название листа!A1",
#												 valueInputOption='',
#												 insertDataOption='', 
#												 body='123').execute()


#Добавление данных в ячейку
results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1RvgTYKbK89KQpqN6nW7w95yBX7BlGXbr3ZjHNgdnQ_o', body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        
		 {"range": "Сие есть название листа!A5",
         "majorDimension": "COLUMNS",  # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
         "values": [["5"]]}
    ]
}).execute()

request = service.spreadsheets().values().update(spreadsheetId='1RvgTYKbK89KQpqN6nW7w95yBX7BlGXbr3ZjHNgdnQ_o', range='A6', valueInputOption='USER_ENTERED', body=['6']).execute()