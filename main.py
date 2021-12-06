from flask import Flask, request, jsonify
from threading import Thread

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

app = Flask('')

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'200',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '60420370-f85d-4c7b-9402-f5b9b8560203',
}

def getDat(coinSym):
  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    # print(data['data'])
    # for key, value in data['data'][1].items():
    #   print(key, value)
    for i in range(200):
      if data['data'][i]['symbol'] == coinSym:
        # print(data['data'][i])
        # for key, value in data['data'][i].items():
        #   print(key, value)
        data_set = {"name": data['data'][i]['name'], "rank": data['data'][i]['cmc_rank'], "price": data['data'][i]['quote']['USD']['price'], "volume_24h": data['data'][i]['quote']['USD']['volume_24h'], "volume_change_24h": data['data'][i]['quote']['USD']['volume_change_24h'], "percent_change_1h": data['data'][i]['quote']['USD']['percent_change_1h'], "percent_change_24h": data['data'][i]['quote']['USD']['percent_change_24h']}
        return json.dumps(data_set)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

@app.route('/coin', methods = ['POST', 'GET'])
def pass_cap():
  if request.method == 'GET':
    try:
      coinSym = request.args.get('symbol', type = str)
      return getDat(coinSym)
    except:
      return "Error"

@app.route('/')
def home():
    return "COIN ARDUINO"

def run():
  app.run(host='0.0.0.0',port=8080)

run()
