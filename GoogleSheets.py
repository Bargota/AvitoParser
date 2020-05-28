import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class myGoogleSheet():
	spreadsheetId = '1QQ72J0T6zZF-CddtOAt9GMdn8Hduc0Wx-IQwr-zUhzI'
	#service

	def __init__(self):
		CREDENTIALS_FILE = 'AvitoParser-fa42c491fb6e.json'  # имя файла с закрытым ключом
		credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
																				  'https://www.googleapis.com/auth/drive'])
		httpAuth = credentials.authorize(httplib2.Http())
		self.service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


	#Создание нового документа
	def CreateSheet(self,name_doc,name_sheet):
		spreadsheet = self.service.spreadsheets().create(body = {
																'properties': {'title': name_doc, 'locale': 'ru_RU'},
																'sheets': [{'properties': {'sheetType': 'GRID',
																							'sheetId': 0,
																							'title': name_sheet,
																							#'gridProperties': {'rowCount': 8, 'columnCount': 5}
																							}}]
															}).execute()

	#Добавление строки данных, если A1 ячейка заполненна данные добавятся в первую незаполненную строку
	def AppendRow(self,range_with_list,row_list):
		results = self.service.spreadsheets().values().append(
												spreadsheetId=self.spreadsheetId,
												range=range_with_list,
												valueInputOption='USER_ENTERED',
												insertDataOption='INSERT_ROWS',
												body = 
														
																	{
																		"range":range_with_list,
																		"majorDimension": "COLUMNS",
																		"values": row_list
																	}
																
														
												).execute()

	#Очистить ячейки
	def ClearSheet(self):
		results = self.service.spreadsheets().values().batchClear(
																spreadsheetId=self.spreadsheetId,
																body={
																		"ranges": ['Смотреть тут!A1:Z10000']
																	 }
															).execute()

	#Добавление данных в ячейку
	def AddData(self,range, data):
		results = self.service.spreadsheets().values().batchUpdate(
																spreadsheetId = self.spreadsheetId,
																body = {
																		"valueInputOption": "USER_ENTERED",
																		"data": [
																					{
																						"range": range,
																						"majorDimension": "ROWS",  # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
																						"values": data
																					}
																				]
																		}
															).execute()

	def ReadData(self,range):
		'''Read data in range'''
		result = self.service.spreadsheets().values().get(spreadsheetId = self.spreadsheetId,
													range=range
												   
													).execute()
		if 'values'in result:
			return result['values']
		else:
			return []




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

#gs=myGoogleSheet()
#gs.AddData('Лист1!A1',
#						[['1','2'],
#						['3','4']]
#					  )




