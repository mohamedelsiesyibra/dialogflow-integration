import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# flask app should start in global 
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")

    r = requests.get('https://samples.openweathermap.org/data/2.5/forecast?q='+city+',us&appid=b6907d289e10d714a6e88b30761fae22')  

    json_object = r.json()
    weather= json_object['list']
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']

    speech = "The Forecast For "+city+" for "+date+" is "+condition
    return {
        "fulfillmentText": speech,
        "text": speech,
        "source": "dialogflow-weather"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
