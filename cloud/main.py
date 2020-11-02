from spreadsheet import Spreadsheet
from run_function import run_functions
import functions
from model import *
from model import MyClassifier
import urllib.parse as urlparse
from urllib.parse import parse_qs

curr_spreadsheet = Spreadsheet()

model = MyClassifier(vectorizer='pretrained_glove_50', spreadsheet=curr_spreadsheet, debug=False)

def text_process(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    request_json = request.get_json()
    text = ""
    url = ""
    if request.args and 'text' in request.args:
        text = request.args.get('text')
    elif request_json and 'text' in request_json:
        text = request_json['text']
 
    if request.args and 'url' in request.args:
        url = request.args.get('url')
    elif request_json and 'url' in request_json:
        url = request_json['url']

    parsed = urlparse.urlparse(url)
    gid = parse_qs(parsed.fragment)['gid'][0]
    vals = url.split("/")
    key = vals[5]

    curr_spreadsheet.set_sheet(key)
    curr_spreadsheet.set_worksheet(gid)
    sheet = curr_spreadsheet.sheet

    model.classify(text)

    ## Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    return ("success", 200, headers)
