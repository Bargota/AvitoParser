import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class myGoogleSheet():
	self.spreadsheetId = '1QQ72J0T6zZF-CddtOAt9GMdn8Hduc0Wx-IQwr-zUhzI'
	self.service

	def __init__(self):
		CREDENTIALS_FILE = 'AvitoParser-fa42c491fb6e.json'  # имя файла с закрытым ключом
		credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
		httpAuth = credentials.authorize(httplib2.Http())
		service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


	#Создание нового документа
	def CreateSheet(self,name_doc,name_sheet):
		spreadsheet = service.spreadsheets().create(body = {
																'properties': {'title': name_doc, 'locale': 'ru_RU'},
																'sheets': [{'properties': {'sheetType': 'GRID',
																							'sheetId': 0,
																							'title': name_sheet,
																							#'gridProperties': {'rowCount': 8, 'columnCount': 5}
																							}}]
															}).execute()




#Создание нового документа
#spreadsheet = service.spreadsheets().create(body = {
#    'properties': {'title': 'Сие есть название документа', 'locale': 'ru_RU'},
#    'sheets': [{'properties': {'sheetType': 'GRID',
#                               'sheetId': 0,
#                               'title': 'Сие есть название листа',
#                               'gridProperties': {'rowCount': 8, 'columnCount': 5}}}]
#}).execute()

#Открытие доступа на редактирование
#Доступ к фйлу через Google Drive API
#driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
#shareRes = driveService.permissions().create(
#    fileId = spreadsheet['spreadsheetId'],
#    #body = {'type': 'user', 'role': 'writer', 'emailAddress': 'v.orlov.geo@gmail.com'}, 
#    body={'type': 'anyone', 'role': 'reader'}, # доступ на чтение кому угодно
#    fields = 'id'
#).execute()



#results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1QQ72J0T6zZF-CddtOAt9GMdn8Hduc0Wx-IQwr-zUhzI', body = {
#    "valueInputOption": "USER_ENTERED",
#    "data": [
#        {"range": "Лист1!A1",
#         "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
#         "values": [["123"]]},

        
#    ]
#}).execute()



#results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet['spreadsheetId'], body = {
#    "valueInputOption": "USER_ENTERED",
#    "data": [
#        {"range": "Сие есть название листа!A1:A2",
#         "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
#         "values": [["This is B3", "This is C2"]]}]}).execute()



#Добавление данных в ячейку
#results = service.spreadsheets().values().batchUpdate(spreadsheetId = '1RvgTYKbK89KQpqN6nW7w95yBX7BlGXbr3ZjHNgdnQ_o', body = {
#    "valueInputOption": "USER_ENTERED",
#    "data": [
        
#		 {"range": "Сие есть название листа!A5",
#         "majorDimension": "COLUMNS",  # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
#         "values": [["5"]]}
#    ]
#}).execute()

#Добавление строки данных, если A1 ячейка заполненна данные добавятся в первую незаполненную строку
results = service.spreadsheets().values().append(
												spreadsheetId='1QQ72J0T6zZF-CddtOAt9GMdn8Hduc0Wx-IQwr-zUhzI',
												range='Лист1!A1',
												valueInputOption='USER_ENTERED',
												insertDataOption='INSERT_ROWS',
												body = 
														
																	{
																		"range": "Лист1!A1",
																		"majorDimension": "COLUMNS",
																		"values": [["345"],["123"]]
																	}
																
														
												).execute()
print(results.get("tableRange"))


#Очистить ячейки
results = service.spreadsheets().values().batchClear(
														spreadsheetId='1QQ72J0T6zZF-CddtOAt9GMdn8Hduc0Wx-IQwr-zUhzI',
													    body={
																"ranges": ['Лист1!A1:Z10000']
															 }
													).execute()


