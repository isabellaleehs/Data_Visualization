# Create choropleth map
#
# Date: Dec 2017

import plotly as py
import pandas as pd
import pycountry

def get_data(filename):
    '''
    Loads data from file and cleans it.

    Inputs:
        filename: file directory

    Returns: a cleaned dataframe
    '''
    df = pd.read_csv(filename)

    # Reset header row
    df.columns = df.iloc[0]    
    df = df[1:] 

    # Rename column
    df = df.rename(index=str, columns={"2016": "Estimated no. w/ HIV"})

    # Remove all parenthesis and square brackets
    df['Country'] = df.Country.apply(lambda x: x.replace(' (',', ').replace(')',''))
    # Alternative to above: df['Country'] = df['Country'].str.replace(r"\s+\((.*)\)", r", \1")
    df['Estimated no. w/ HIV'] = df['Estimated no. w/ HIV'].str.replace(r"\s+\[.*\]","")

    # Lower case, remove spaces between numbers, remove strings and set to 0
    df['Estimated no. w/ HIV'] = df['Estimated no. w/ HIV'].str.replace(" ","")
    df['Estimated no. w/ HIV'] = df['Estimated no. w/ HIV'].str.strip("<>")
    df['Estimated no. w/ HIV'] = df['Estimated no. w/ HIV'].str.replace("Nodata","")

    # Modify names of countries not recognized by pycountry
    df['Country'] = df['Country'].replace('Democratic Republic of the Congo','Congo, the Democratic Republic of the')
    df['Country'] = df['Country'].replace('Republic of Korea',"Korea, Democratic People's Republic of")
    return df


def get_country_code(x):
    '''
    Finds the 3 letter alpha code for a country.

    Inputs:
        x: country name

    Returns: alpha_3 code for the country
    '''
    if pycountry.countries.lookup(x) != None:
        return pycountry.countries.lookup(x).alpha_3


# Get and clean data
df = get_data('data.csv')
df['Code'] = df['Country'].apply(get_country_code)

# Make choropleth map using data
data = [ dict(
        type = 'choropleth',
        locations = df['Code'],
        z = df['Estimated no. w/ HIV'],
        text = df['Country'],
        colorscale = [[0,"#c6dbef"],[0.2,"#6baed6"],[0.4,"#4292c6"],\
            [0.6,"#2171b5"],[0.8,"#0e5693"],[1,"#013e7c"]],
        autocolorscale = False,
        reversescale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Estimated no.<br>w/ HIV'),
      ) ]

layout = dict(
    title = 'Number of people (all ages) living with HIV<br>Estimates by country<br><br>\
            [Source:<a href="http://apps.who.int/gho/data/node.main.620?lang=en"> World Health Organization</a>]',
    margin = dict(
        l=10,
        r=10,
        b=50,
        t=150,
        pad=4
    ),
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

# Display map
fig = dict( data=data, layout=layout )
py.offline.plot( fig, validate=False, filename='d3-world-map' )
