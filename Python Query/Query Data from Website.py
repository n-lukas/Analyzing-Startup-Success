import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

webpage_response = requests.get('https://www.cbinsights.com/research-unicorn-companies')
webpage = webpage_response.content
soup = bs(webpage, "html.parser")
tables = soup.find_all('table')

Companies = []
Valuations = []
Dates = []
Countries = []
Cities = []
Industries = []

for tr in tables[0].find_all('tr'):
    td = tr.find_all('td')
    if not td:
        continue
    company, valuation, date, country, city, industry = [td.text.strip() for td in td[0:6]]
    Companies.append(company)
    Valuations.append(valuation)
    Dates.append(date)
    Countries.append(country)
    Cities.append(city)
    Industries.append(industry)

data = {'Company': Companies, 'Valuation': Valuations, 'Date': Dates, 'Country': Countries, 'City': Cities, 'Industry': Industries}
Startups = pd.DataFrame(data)
