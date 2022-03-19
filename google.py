from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time

gscope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gcredentials = 'db-api.json'
gdocument = 'DataBase Taff'

credentials = ServiceAccountCredentials.from_json_keyfile_name(gcredentials, gscope)
gc = gspread.authorize(credentials)
wks = gc.open(gdocument).sheet1
#wks.append_row(
  #      ['колонка1', 'колонка2', 'колонка3', 'колонка4'])

get_data = wks.get_all_records()

for row in get_data:
	if 'колонка21' in row:
		print(row)