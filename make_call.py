from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np



app = Flask(__name__)

@app.route("/voice", methods=['GET','POST'])
def voice():
    resp = VoiceResponse()

    resp.say('Hey beautiful say a country and we will tell you how they are doing now during this quarantine')
    resp.gather(input='speech',speechTimeout=1, action='/test')
    
    return str(resp)


@app.route("/test", methods=['GET','POST'])
def test():
    df = data()
    resp = VoiceResponse()  
    if 'SpeechResult' in request.values:
        speech = request.values['SpeechResult'].lower()

        if speech in list(df['Country']):
            #row = df.loc[df['Country'] == speech]
            country = speech
            total_cases = df.loc[df.Country == speech,'TotalCases'].tolist()[0]
            total_deaths = df.loc[df.Country == speech,'TotalDeaths'].tolist()[0]
            
            say_this = country + ' has ' + str(total_cases)+ ' Total cases'
            say_this += ' but only ' + str(total_deaths) + ' deaths'
            say_this += 'so stay blessed and wash your hands, this will be over in a blink of an eye'
            print(say_this)
            resp.say(say_this)
            resp.redirect('/voice')
            
        else:
            resp.say('Sorry I didnt understand what you said, im not that smart')
            resp.redirect('/voice')



    return str(resp)

def data():
    #----------SCRAPING ON WEBSITE BELOW TO FIND TOP COUNTRIES DEALING WITH CORONA
    URL = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    columns = ['Country', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases', 'SeriousCritical','9','10','11','12']
    df = pd.DataFrame(columns=columns)


    table = soup.find('table', attrs={'id':'main_table_countries_today'}).tbody
    trs = table.find_all('tr')

    for tr in trs:
        tds = tr.find_all(['th','td'])
        row = [td.text.replace('\n', '') for td in tds]
        df = df.append(pd.Series(row,index=columns), ignore_index=True)
    
    annoying_characters = ','
    df = (df.replace(" ",np.nan,inplace=False))
    df = (df.replace("",np.nan,inplace=False))

    df = (df.fillna(0))
    df['TotalCases'] = df['TotalCases'].str.replace(annoying_characters, '').astype('float')
    df['TotalDeaths'] = df['TotalDeaths'].str.replace(annoying_characters, '').astype('float')
    df['ActiveCases'] = df['ActiveCases'].str.replace(annoying_characters, '').astype('float')
    df['SeriousCritical'] = df['SeriousCritical'].str.replace(annoying_characters, '').astype('float')
    
    for index, row in df.iterrows():
        row = row['Country'].lower()
        df.at[index,'Country'] = df.at[index,'Country'].lower()
    print(df)
    return df
    
if __name__ =='__main__':
    app.run(debug=True)
