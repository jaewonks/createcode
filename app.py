from flask import Flask, render_template, request, jsonify
import sys

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

application = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
json_file_name = './ecountproject-65a3a002b9e0.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1EjgZZ6Z1O2-0gPnORQXVFCjK5Cu9GmA96Y5Mcrmn0bE/edit#gid=1146862970'

# 문서 불러오기
doc = gc.open_by_url(spreadsheet_url)
# createcode 시트 불러오기
worksheet = doc.worksheet('createcode')

# a 시트 불러오기,cell_data = worksheet.acell('C2').value
request_url = "https://openapi.naver.com/v1/papago/n2mt"

@application.route('/')
def index():
  return render_template('index.html')

@application.route('/trans', methods=['GET'])
def trans():
  if request.method == 'GET':
    start = request.args.get('start')
    end = request.args.get('end')
    print(str(start+':'+end))
    range_list = worksheet.range(str(start+':'+end))
    for cell in range_list:
      # print(cell.value)
      text = cell.value

      headers = {"X-Naver-Client-Id": "2Cudld_dW4HaSzleLPTT", "X-Naver-Client-Secret": "3VnQ1L_7Ld"}
      params = {"source": "ko", "target": "en", "text": text}
      response = requests.post(request_url, headers=headers, data=params)
      result = response.json()
      result1 = result['message']['result']['translatedText']
      print(result1.upper())
    return result1.upper()

if __name__ == '__main__':
  application.run(host='0.0.0.0', port=5000)
