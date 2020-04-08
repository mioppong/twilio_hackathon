from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests



app = Flask(__name__)

@app.route("/voice", methods=['GET','POST'])
def voice():
    resp = VoiceResponse()

    resp.say('Hey, handsome and or beautiful say a country and we will tell you how they are doing now during this quarantine', language='es-ES')
    resp.gather(input='speech',speechTimeout=2, action='/test')
    
    return str(resp)


@app.route("/test", methods=['GET','POST'])
def test():
    df = data()
    print(df)
    resp = VoiceResponse()  
    answer = 10
    if 'SpeechResult' in request.values:
        speech = request.values['SpeechResult'].lower()


        if speech == 'apple':
            resp.say("Canada has" + str(answer) + 'cases')


    return str(resp)

def data():
    #----------SCRAPING ON WEBSITE BELOW TO FIND TOP COUNTRIES DEALING WITH CORONA
    URL = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    columns = ['CountryOther', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases', 'SeriousCritical','9','10','11','12']
    df = pd.DataFrame(columns=columns)


    table = soup.find('table', attrs={'id':'main_table_countries_today'}).tbody
    trs = table.find_all('tr')

    for tr in trs:
        tds = tr.find_all(['th','td'])
        row = [td.text.replace('\n', '') for td in tds]
        df = df.append(pd.Series(row,index=columns), ignore_index=True)
    
    annoying_characters = ',+'
    df['TotalCases'] = df['TotalCases'].str.replace(annoying_characters, '').astype(float)
    df['TotalDeaths'] = df['TotalDeaths'].str.replace(annoying_characters, '').astype(float)
    df['ActiveCases'] = df['ActiveCases'].str.replace(annoying_characters, '').astype(float)
    df['SeriousCritical'] = df['SeriousCritical'].str.replace(annoying_characters, '').astype(float)


    return df
    
if __name__ =='__main__':
    app.run(debug=True)
