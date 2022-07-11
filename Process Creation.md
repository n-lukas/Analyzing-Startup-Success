## Querying Data

Data was queried using Python directly into Power BI

Importing Libraries:
`import numpy as np`
`import pandas as pd`
`from bs4 import BeautifulSoup as bs`
`import requests`

Getting data from website:
`webpage_response = requests.get('https://www.cbinsights.com/research-unicorn-companies')`
`webpage = webpage_response.content`
`soup = bs(webpage, "html.parser")`
`tables = soup.find_all('table')`

Defining variables for data we need:
`Companies = []`
`Valuations = []`
`Dates = []`
`Countries = []`
`Cities = []`
`Industries = []`

Filling variables with data from website:
`for tr in tables[0].find_all('tr'):`
`    td = tr.find_all('td')`
`    if not td:`
`        continue`
`    company, valuation, date, country, city, industry = [td.text.strip() for td in td[0:6]]`
`    Companies.append(company)`
`    Valuations.append(valuation)`
`    Dates.append(date)`
`    Countries.append(country)`
`    Cities.append(city)`
`    Industries.append(industry)`


Turning Data into Table:
`data = {'Company': Companies, 'Valuation': Valuations, 'Date': Dates, 'Country': Countries, 'City': Cities, 'Industry': Industries}`
`Startups = pd.DataFrame(data)`

![Query](Analyzing-Startup-Success/blob/master/Process Screenshots/Querying Data using Python and Power BI.png)

## Transforming Data

Importing data for nearest major city `.../CSV Data/Major Cities Lookup.CSV`
Based on US Census Data Metro/Micro Statistical Area 2021

Created realtionships in data model using `City` in the `Startups` table as the primary key and `City` in the `Major Cities Lookup` table as the foreign key.

![Transform](Analyzing-Startup-Success/blob/master/Process Screenshots/Data Model.png)

Added the following DAX formulas to create a new column in the primary table
`Major City Location = RELATED('Major Cities Lookup'[Major City]) & ", " & RELATED('Major Cities Lookup'[State]) & ", " & 'Startups'[Country]`

This provide a clean concatinated locations that allows us to look up the location on map visuals and ensure it is pulling correctly.

Created a DAX formula to calculate average startup value
`Average Startup Value = CALCULATE(DIVIDE(SUM('Startups'[Valuation]), COUNTA('Startups'[Company])))`
This gives us an average startup value per city and an average startup value per industry.

## Visualizing Data

### Dashboard
![Dashboard]()
The dashboard shows the high level overview of the data. On the top you have Valuation, Average Startup Value and number of startups.
The column the very left shows industries while the column to the very right shows cities and states. You can click on any of these items and the key metrics will change in regard to what is selected.
The center buttons act as a central way to quickly find the details of the data you are looking for.

Two DAX formulas were used to create calcualted measures used only on the dashboard. The reason for this is purely aesthetic and allows the visuals to show true values. This also lets the user know the scope of the values on the remainder of the report.
`Actual Average Startup Value = (CALCULATE(DIVIDE(SUM('Startups'[Valuation]), COUNTA('Startups'[Company])))) * 1000000000`
`Actual Valuation = CALCULATE(SUM('Startups'[Valuation]) * 1000000000)`

### By City
![Cities]()
#### Map
A map was used here due to data being location based. Sicne we are dealing with major cities, you are able to quickly see which cities have the highest valuation, # of startups, and succcess. 
The displayed metric can be changed between valuation, number of startups, and value/startup using the buttons provided. 
#### Table
A table was used to summarize the data in an easy to read numerical format. Using the buttons will sort the data by the selected value in descending order

### By Industry
![Industries]()
#### Tree Map
A tree map was used to show the proportion of industries that make up the key metrics. Similar to the City tab, buttons can be used here to change which metric is being displayed.
#### Table
Similarly to the City tab, a table is used here to display easy to read numericals. 

### By both City and Industry
![Industry by City]()
##### Clustered Bar Chart
Due to the large amount of data, a clustered bar chart was used. You can quickly find which industries are the most prevelant in which cities by looking at the size of the bar. Values are also displayed on the bottom.
##### Matrix
A matrix was used to show the full picture of success by city and industry. The intersections show the value/startup for each city and industry. Totals are used to show the total startup/value by city and industry as well. Any blank data means that the industry is not present in that city.

### Relationships
![Interactions]()
You can click on any of the data points and it will automatically filter the rest of the data on that tab by that point
![Drill Down]()
You can drill down to company level and see which values make up the key metric
![Slicer]()
You can filter by city on the Industries tab to have an additional set of visuals for key metrics by both industry and city.