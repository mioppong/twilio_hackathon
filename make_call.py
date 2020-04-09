from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests
import random
import numpy as np

#----- a list of positive sentences to tell user
#----- after i have told them the number of cases and deaths
#----- the country they specified has
positive_sentences = ['this will be over in a blink of an eye','pray and hope for the best','dont stress, this will all be over soon','hope you have a great day, you deserve it', 'call all your family and friends and tell them you love them']


app = Flask(__name__)

#----- main function, gets input from user, and sends the
#----- user to the function (/test), which then does the major work
@app.route("/voice", methods=['GET','POST'])
def voice():
    resp = VoiceResponse()
    resp.say('Hey beautiful say a country or continent we will tell you their corona stats, Say one country and say it clear')
    resp.gather(input='speech',speechTimeout=1, action='/test')
    return str(resp)



#-----this method gets the country said by the user, then it searches through 
#----- the df dataframe for the country specified
#----- tells the user, and redirects them to the main menu/function, (/voice)
@app.route("/test", methods=['GET','POST'])
def test():
    df = data()
    resp = VoiceResponse()  

    if 'SpeechResult' in request.values:
        speech = request.values['SpeechResult'].lower()

        if speech in list(df['Country']):
            country = speech

            total_cases = df.loc[df.Country == speech,'TotalCases'].tolist()[0]
            total_deaths = df.loc[df.Country == speech,'TotalDeaths'].tolist()[0]
            
            say_this = country + ' has ' + str(total_cases)+ ' Total cases'
            say_this += ' but only ' + str(total_deaths) + ' deaths'
            say_this += positive_sentences[random.randrange(0,len(positive_sentences))]
            
            resp.say(say_this)
            resp.redirect('/voice')
            
        else:
            resp.say('Sorry I didnt understand what you said')
            resp.redirect('/voice')



    return str(resp)

#----- this method scrapes a website to gather information on 
#----- a countries stats during the corona virus
#----- they tend to update the website every couple days, adding new features to the 
#----- table, so sometimes i might need to update how i screape and clean the dataset
def data():
    #----------SCRAPING ON WEBSITE BELOW TO FIND TOP COUNTRIES DEALING WITH CORONA
    URL = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    columns = ['Country', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases', 'SeriousCritical','9','10','11','12','13']
    df = pd.DataFrame(columns=columns)


    table = soup.find('table', attrs={'id':'main_table_countries_today'}).tbody
    trs = table.find_all('tr')

    for tr in trs:
        tds = tr.find_all(['th','td'])
        row = [td.text.replace('\n', '') for td in tds]
        df = df.append(pd.Series(row,index=columns), ignore_index=True)
    
    #----- this is how i clean empty data sets
    #----- i repalce them with 0 
    df = df[df.Country != '']
    df = df[df.Country != 0]
    annoying_characters = ','
    df = (df.replace(" ",np.nan,inplace=False))
    df = (df.replace("",np.nan,inplace=False))
    df = (df.fillna(0))

    #these are the stats i planned on telling the user
    df['TotalCases'] = df['TotalCases'].str.replace(annoying_characters, '').astype('float')
    df['TotalDeaths'] = df['TotalDeaths'].str.replace(annoying_characters, '').astype('float')
    df['ActiveCases'] = df['ActiveCases'].str.replace(annoying_characters, '').astype('float')
    df['SeriousCritical'] = df['SeriousCritical'].str.replace(annoying_characters, '').astype('float')
    
    #----- making all the countries lowercase 
    #----- so i can search through them
    for index, row in df.iterrows():
        row = row['Country'].lower()
        df.at[index,'Country'] = df.at[index,'Country'].lower()
    
    return df
    
if __name__ =='__main__':
    app.run(debug=True)
