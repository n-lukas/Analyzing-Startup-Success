## Querying Data

Data was queried using Python directly into Power BI

Importing Libraries: <br />
`import numpy as np` <br />
`import pandas as pd` <br />
`from bs4 import BeautifulSoup as bs` <br />
`import requests` <br />

Getting data from website: <br />
`webpage_response = requests.get('https://www.cbinsights.com/research-unicorn-companies')` <br />
`webpage = webpage_response.content` <br />
`soup = bs(webpage, "html.parser")` <br />
`tables = soup.find_all('table')` <br />

Defining variables for data we need: <br />
`Companies = []` <br />
`Valuations = []` <br />
`Dates = []` <br />
`Countries = []` <br />
`Cities = []` <br />
`Industries = []` <br />

Filling variables with data from website: <br />
`for tr in tables[0].find_all('tr'):` <br />
`    td = tr.find_all('td')` <br />
`    if not td:` <br />
`        continue` <br />
`    company, valuation, date, country, city, industry = [td.text.strip() for td in td[0:6]]` <br />
`    Companies.append(company)` <br />
`    Valuations.append(valuation)` <br />
`    Dates.append(date)` <br />
`    Countries.append(country)` <br />
`    Cities.append(city)` <br />
`    Industries.append(industry)` <br />


Turning Data into Table: <br />
`data = {'Company': Companies, 'Valuation': Valuations, 'Date': Dates, 'Country': Countries, 'City': Cities, 'Industry': Industries}` <br />
`Startups = pd.DataFrame(data)` <br />

![Query](Process Screenshots/Querying Data using Python and Power BI.PNG)

## Transforming Data

Importing data for nearest major city `.../CSV Data/Major Cities Lookup.CSV`
Based on US Census Data Metro/Micro Statistical Area 2021

Created realtionships in data model using `City` in the `Startups` table as the primary key and `City` in the `Major Cities Lookup` table as the foreign key.

![Transform](Process Screenshots/Data Model.PNG)

Added the following DAX formulas to create a new column in the primary table
`Major City Location = RELATED('Major Cities Lookup'[Major City]) & ", " & RELATED('Major Cities Lookup'[State]) & ", " & 'Startups'[Country]`

This provide a clean concatinated locations that allows us to look up the location on map visuals and ensure it is pulling correctly.

Created a DAX formula to calculate average startup value
`Average Startup Value = CALCULATE(DIVIDE(SUM('Startups'[Valuation]), COUNTA('Startups'[Company])))`
This gives us an average startup value per city and an average startup value per industry.

## Visualizing Data

### Dashboard
![Dashboard](Visualizations/Dashboard.PNG)
The dashboard shows the high level overview of the data. On the top you have Valuation, Average Startup Value and number of startups.
The column the very left shows industries while the column to the very right shows cities and states. You can click on any of these items and the key metrics will change in regard to what is selected.
The center buttons act as a central way to quickly find the details of the data you are looking for.

Two DAX formulas were used to create calcualted measures used only on the dashboard. The reason for this is purely aesthetic and allows the visuals to show true values. This also lets the user know the scope of the values on the remainder of the report. <br />
`Average Startup Valuation = (CALCULATE(DIVIDE(SUM('Startups'[Valuation]), COUNTA('Startups'[Company])))) * 1000000000` <br />
`Total Startup Valuation = CALCULATE(SUM('Startups'[Valuation]) * 1000000000)` 

### By City
![Cities](Visualizations/Cities.PNG)
#### Map
A map was used here due to data being location based. Sicne we are dealing with major cities, you are able to quickly see which cities have the highest valuation, # of startups, and succcess. 
The displayed metric can be changed between valuation, number of startups, and value/startup using the buttons provided. 
#### Table
A table was used to summarize the data in an easy to read numerical format. Using the buttons will sort the data by the selected value in descending order

### By Industry
![Industries](Visualizations/Industries.PNG)
#### Tree Map
A tree map was used to show the proportion of industries that make up the key metrics. Similar to the City tab, buttons can be used here to change which metric is being displayed.
#### Table
Similarly to the City tab, a table is used here to display easy to read numericals. 

### By both City and Industry
![Industries](Visualizations/Industry by City.PNG)
##### Clustered Bar Chart
Due to the large amount of data, a clustered bar chart was used. You can quickly find which industries are the most prevelant in which cities by looking at the size of the bar. Values are also displayed on the bottom.
##### Matrix
A matrix was used to show the full picture of success by city and industry. The intersections show the value/startup for each city and industry. Totals are used to show the total startup/value by city and industry as well. Any blank data means that the industry is not present in that city.

### Relationships
![Tooltips](Visualizations/Tooltip.PNG)
Highlighting a city or industry on the dashboard or Industry by City page will show a pop out of their respected report (Cities or Industries) with data portaining only to the highlighted selection
![Interactions](Visualizations/Interactions.PNG)
You can click on any of the data points and it will automatically filter the rest of the data on that tab by that point
![Drill](Visualizations/Drill Down.PNG)
You can drill down to company level and see which values make up the key metric
![Interactions](Visualizations/Slicer.PNG)
You can filter by city on the Industries tab to have an additional set of visuals for key metrics by both industry and city.