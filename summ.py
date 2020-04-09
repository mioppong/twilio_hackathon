from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np



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
print(df)
df = (df.replace(" ",np.nan,inplace=False))
df = (df.replace("",np.nan,inplace=False))

df['TotalDeaths'] = df['TotalDeaths'].str.replace(annoying_characters, '').astype('float')
for index, row in df.iterrows():
    row = row['Country'].lower()
    df.at[index,'Country'] = df.at[index,'Country'].lower()

print(df)