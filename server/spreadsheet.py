import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

class Spreadsheet:
    def __init__(self):
        self.sheetId = None
        self.worksheetId = None
        self.authorize()
        self.curr_gs = None
        self.sheet = None

    def authorize(self):
        scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

        self.client = gspread.authorize(creds)

    def set_sheet(self, sheetId):
        if(sheetId != self.sheetId):
            self.sheetId = sheetId
            self.curr_gs = self.client.open_by_key(self.sheetId)

    def set_worksheet(self, worksheetId):
        if(worksheetId != self.worksheetId):
            self.worksheetId = worksheetId
            self.select_worksheet_by_gid()
    
    def select_worksheet_by_gid(self):
        for sheet in self.curr_gs.worksheets():
            if sheet.id == int(self.worksheetId):
                self.sheet = sheet
                break