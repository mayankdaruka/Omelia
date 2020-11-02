from model import MyClassifier
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import urllib.parse as urlparse
from urllib.parse import parse_qs
from spreadsheet import Spreadsheet
from run_function import run_functions
import functions
from flask_cors import CORS
from model import *

app = Flask(__name__)
# cors = CORS(app)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
api = Api(app)
CORS(app, origins="http://127.0.0.1:8080", allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)

spreadsheet_args = reqparse.RequestParser()
spreadsheet_args.add_argument("text", type=str, required=True)
spreadsheet_args.add_argument("url", type=str, required=True)

curr_spreadsheet = Spreadsheet()

model = MyClassifier(vectorizer='pretrained_glove_50', spreadsheet=curr_spreadsheet, debug=False)

class SpreadsheetManager(Resource):
    def post(self):
        args = spreadsheet_args.parse_args()
        url = args["url"]
        text = args["text"]


        # get sheet number
        parsed = urlparse.urlparse(url)
        gid = parse_qs(parsed.fragment)['gid'][0]

        # get spreadsheet key
        vals = url.split("/")
        key = vals[5]
        print(vals)
        print(key)

        # set sheet and worksheet
        curr_spreadsheet.set_sheet(key)
        curr_spreadsheet.set_worksheet(gid)
        sheet = curr_spreadsheet.sheet

        model.classify(text)
        # functions.add(curr_spreadsheet.sheet, 100, 'B2')
        # functions.set_background(curr_spreadsheet.sheet, "A1:B2", "blue")
        # functions.insert(sheet, 1, 1)
        # functions.multiply_range(sheet, 2, "B2:B5")
        # functions.multiply_entry(sheet, 2, 2, 1)
        # functions.update_cell_literal(sheet, 2, 2, 100)
        # functions.update_range(sheet, "B2:B5", 2)
        # functions.format_bold(sheet, "B2:B5")
        # print(functions.average_entry(sheet, 2, 1))
        # functions.sin_range(sheet, "B2:B4")
        # functions.sin_entry(sheet, 2, 1)
        # if("sort" in text):
        #     functions.sort(sheet, (int(text[-1]), 'asc'))
        # if("bold" in text):
        #   functions.bold(sheet, text[-1])
        # text = args["text"]
        # print(text)
        # functions.addNumEntry(sheet, 2, 2, 1)
        
        return {"success": True}


api.add_resource(SpreadsheetManager, "/")

if __name__ == "__main__":
  app.run(debug=True)
 