import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import functions

# scope = ["https://spreadsheets.google.com/feeds",'https://https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

spread_sheet_name = "excelify-test"
spread_sheet = client.open(spread_sheet_name)
sheet = spread_sheet.sheet1 
# checkpoint
print(spread_sheet.worksheets())
data = sheet.get_all_records()
pprint(data)

#checkpoint - print stuff

row = sheet.row_values(3)
col = sheet.col_values(2)
cell = sheet.cell(1,2).value
pprint(row)
pprint(col)
pprint(cell)


sheet2 = client.open_by_url("https://docs.google.com/spreadsheets/d/1K8n-Bcn9uqcuNXfVG4PA2zgDvNIUG5bUyh54CescYVc/edit?ts=5f944b9b#gid=0").sheet1

print(sheet2.get_all_records())

# #checkpoint - insert row
# insertRow = ["hello", 5, "red", "blue"]
# sheet.insert_row(insertRow, 4)

# #checkpoint - delete row
# sheet.delete_row(3)

# #checkpoint - update
# sheet.update_cell(8,2, "changed")
sheet.update("b1", "222")

numrows = sheet.row_count
pprint(numrows)


