import streamlit as st
import numpy as np
import pandas as pd
import requests
import io
import datetime
import altair as alt
import os
from streamlit.components.v1 import html
st.set_page_config(page_title='Correlation Explorer', layout="wide")

def calculate_pearsons(series1, series2):
    return np.corrcoef(series1, series2)[0, 1]

######
## The below section pulls data from various sources
######

@st.cache_data
def get_umich_data(series='ics'):

    print('Not cached - UMich data')

    if series == 'ics':
        index_col = 'Index'
        umich = requests.post('https://data.sca.isr.umich.edu/data-archive/mine.php', data={'table': 1, 'year': 1978, 'qorm': 'M', 'order': 'asc', 'format': 'Comma-Separated (CSV)'}).text
        df = pd.read_csv(io.StringIO(umich), header=1, usecols=['Month', 'Year', index_col], index_col=False)
    elif series == 'ice':
        index_col = 'Expected Index'
        umich = requests.post('https://data.sca.isr.umich.edu/data-archive/mine.php', data={'table': 5, 'year': 1978, 'qorm': 'M', 'order': 'asc', 'format': 'Comma-Separated (CSV)'}).text
        df = pd.read_csv(io.StringIO(umich), header=1, usecols=['Month', 'Year', index_col], index_col=False)
    elif series == 'icc':
        index_col = 'Current Index'
        umich = requests.post('https://data.sca.isr.umich.edu/data-archive/mine.php', data={'table': 5, 'year': 1978, 'qorm': 'M', 'order': 'asc', 'format': 'Comma-Separated (CSV)'}).text
        df = pd.read_csv(io.StringIO(umich), header=1, usecols=['Month', 'Year', index_col], index_col=False)


    df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1)).dt.strftime('%Y-%m')
    df = df.drop(columns=['Month', 'Year'], axis=1).rename(columns={index_col: 'value'})
    return df.to_dict(orient='records')

@st.cache_data
def get_conference_board_leading_indicators_data(exact_date=True):

    print('Not cached - Conf. Board data')

    # From https://www.investing.com/economic-calendar/cb-consumer-confidence-48

    # Run this on the page:

    # y = [];
    # for (i=1; i < x.querySelectorAll('tbody tr').length; i++) {
    #     if (x.querySelectorAll('tbody tr')[i].getElementsByTagName('td')[0].innerText == 'Jan 01, 2008 (Dec)') {break;}
    #     y.push({'date': x.querySelectorAll('tbody tr')[i].getElementsByTagName('td')[0].innerText.split(" (")[0], 'value': parseFloat(x.querySelectorAll('tbody tr')[i-1].getElementsByTagName('td')[4].innerText)});
    # }

    data_series = [{'date': '2008-02-26', 'value': 75.0}, {'date': '2008-03-25', 'value': 64.5}, {'date': '2008-04-29', 'value': 62.3}, {'date': '2008-05-27', 'value': 57.2}, {'date': '2008-06-24', 'value': 50.4}, {'date': '2008-07-29', 'value': 51.9}, {'date': '2008-08-26', 'value': 56.9}, {'date': '2008-09-30', 'value': 59.8}, {'date': '2008-10-28', 'value': 38.0}, {'date': '2008-11-25', 'value': 44.9}, {'date': '2008-12-30', 'value': 38.0}, {'date': '2009-01-27', 'value': 37.7}, {'date': '2009-02-24', 'value': 25.0}, {'date': '2009-03-31', 'value': 26.9}, {'date': '2009-04-28', 'value': 40.8}, {'date': '2009-05-26', 'value': 54.8}, {'date': '2009-06-30', 'value': 49.3}, {'date': '2009-07-28', 'value': 47.4}, {'date': '2009-08-25', 'value': 54.5}, {'date': '2009-09-29', 'value': 53.4}, {'date': '2009-10-27', 'value': 48.7}, {'date': '2009-11-24', 'value': 50.6}, {'date': '2009-12-29', 'value': 53.6}, {'date': '2010-01-26', 'value': 56.5}, {'date': '2010-02-23', 'value': 46.4}, {'date': '2010-03-30', 'value': 52.3}, {'date': '2010-04-27', 'value': 57.7}, {'date': '2010-05-25', 'value': 62.7}, {'date': '2010-06-29', 'value': 54.3}, {'date': '2010-07-27', 'value': 51.0}, {'date': '2010-08-31', 'value': 53.2}, {'date': '2010-09-28', 'value': 48.6}, {'date': '2010-10-26', 'value': 49.9}, {'date': '2010-11-30', 'value': 54.3}, {'date': '2010-12-28', 'value': 53.3}, {'date': '2011-01-25', 'value': 64.8}, {'date': '2011-02-22', 'value': 72.0}, {'date': '2011-03-29', 'value': 63.8}, {'date': '2011-04-26', 'value': 66.0}, {'date': '2011-05-31', 'value': 61.7}, {'date': '2011-06-28', 'value': 57.6}, {'date': '2011-07-26', 'value': 59.2}, {'date': '2011-08-30', 'value': 45.2}, {'date': '2011-09-27', 'value': 46.4}, {'date': '2011-10-25', 'value': 40.9}, {'date': '2011-11-29', 'value': 55.2}, {'date': '2011-12-27', 'value': 64.8}, {'date': '2012-01-31', 'value': 61.5}, {'date': '2012-02-28', 'value': 71.6}, {'date': '2012-03-27', 'value': 69.5}, {'date': '2012-04-24', 'value': 68.7}, {'date': '2012-05-29', 'value': 64.4}, {'date': '2012-06-26', 'value': 62.7}, {'date': '2012-07-31', 'value': 65.4}, {'date': '2012-08-28', 'value': 61.3}, {'date': '2012-09-25', 'value': 68.4}, {'date': '2012-11-01', 'value': 73.1}, {'date': '2012-11-27', 'value': 71.5}, {'date': '2012-12-27', 'value': 66.7}, {'date': '2013-01-29', 'value': 58.4}, {'date': '2013-02-26', 'value': 68.0}, {'date': '2013-03-26', 'value': 61.9}, {'date': '2013-04-30', 'value': 69.0}, {'date': '2013-05-28', 'value': 74.3}, {'date': '2013-06-25', 'value': 82.1}, {'date': '2013-07-30', 'value': 81.0}, {'date': '2013-08-27', 'value': 81.8}, {'date': '2013-09-24', 'value': 80.2}, {'date': '2013-10-29', 'value': 72.4}, {'date': '2013-11-26', 'value': 72.0}, {'date': '2013-12-31', 'value': 77.5}, {'date': '2014-01-28', 'value': 79.4}, {'date': '2014-02-25', 'value': 78.3}, {'date': '2014-03-25', 'value': 83.9}, {'date': '2014-04-29', 'value': 81.7}, {'date': '2014-05-27', 'value': 82.2}, {'date': '2014-06-24', 'value': 86.4}, {'date': '2014-07-29', 'value': 90.3}, {'date': '2014-08-26', 'value': 93.4}, {'date': '2014-09-30', 'value': 89.0}, {'date': '2014-10-28', 'value': 94.1}, {'date': '2014-11-25', 'value': 91.0}, {'date': '2014-12-30', 'value': 93.1}, {'date': '2015-01-27', 'value': 103.8}, {'date': '2015-02-24', 'value': 98.8}, {'date': '2015-03-31', 'value': 101.4}, {'date': '2015-04-28', 'value': 94.3}, {'date': '2015-05-26', 'value': 94.6}, {'date': '2015-06-30', 'value': 99.8}, {'date': '2015-07-28', 'value': 91.0}, {'date': '2015-08-25', 'value': 101.3}, {'date': '2015-09-29', 'value': 102.6}, {'date': '2015-10-27', 'value': 99.1}, {'date': '2015-11-24', 'value': 92.6}, {'date': '2015-12-29', 'value': 96.3}, {'date': '2016-01-26', 'value': 97.8}, {'date': '2016-02-23', 'value': 94.0}, {'date': '2016-03-29', 'value': 96.1}, {'date': '2016-04-26', 'value': 94.7}, {'date': '2016-05-31', 'value': 92.4}, {'date': '2016-06-28', 'value': 97.4}, {'date': '2016-07-26', 'value': 96.7}, {'date': '2016-08-30', 'value': 101.8}, {'date': '2016-09-27', 'value': 103.5}, {'date': '2016-10-25', 'value': 100.8}, {'date': '2016-11-29', 'value': 109.4}, {'date': '2016-12-27', 'value': 113.3}, {'date': '2017-01-31', 'value': 111.6}, {'date': '2017-02-28', 'value': 116.1}, {'date': '2017-03-28', 'value': 124.9}, {'date': '2017-04-25', 'value': 119.4}, {'date': '2017-05-30', 'value': 117.6}, {'date': '2017-06-27', 'value': 117.3}, {'date': '2017-07-25', 'value': 120.0}, {'date': '2017-08-29', 'value': 120.4}, {'date': '2017-09-26', 'value': 120.6}, {'date': '2017-10-31', 'value': 126.2}, {'date': '2017-11-28', 'value': 128.6}, {'date': '2017-12-27', 'value': 123.1}, {'date': '2018-01-30', 'value': 124.3}, {'date': '2018-02-27', 'value': 130.0}, {'date': '2018-03-27', 'value': 127.0}, {'date': '2018-04-24', 'value': 125.6}, {'date': '2018-05-29', 'value': 128.8}, {'date': '2018-06-26', 'value': 127.1}, {'date': '2018-07-31', 'value': 127.9}, {'date': '2018-08-28', 'value': 134.7}, {'date': '2018-09-25', 'value': 135.3}, {'date': '2018-10-30', 'value': 137.9}, {'date': '2018-11-27', 'value': 136.4}, {'date': '2018-12-27', 'value': 126.6}, {'date': '2019-01-29', 'value': 121.7}, {'date': '2019-02-26', 'value': 131.4}, {'date': '2019-03-26', 'value': 124.1}, {'date': '2019-04-30', 'value': 129.2}, {'date': '2019-05-28', 'value': 131.3}, {'date': '2019-06-25', 'value': 124.3}, {'date': '2019-07-30', 'value': 135.8}, {'date': '2019-08-27', 'value': 134.2}, {'date': '2019-09-24', 'value': 126.3}, {'date': '2019-10-29', 'value': 126.1}, {'date': '2019-11-26', 'value': 126.8}, {'date': '2019-12-31', 'value': 128.2}, {'date': '2020-01-28', 'value': 130.4}, {'date': '2020-02-25', 'value': 132.6}, {'date': '2020-03-31', 'value': 118.8}, {'date': '2020-04-28', 'value': 85.7}, {'date': '2020-05-26', 'value': 85.9}, {'date': '2020-06-30', 'value': 98.3}, {'date': '2020-07-28', 'value': 91.7}, {'date': '2020-08-25', 'value': 86.3}, {'date': '2020-09-29', 'value': 101.3}, {'date': '2020-10-27', 'value': 101.4}, {'date': '2020-11-24', 'value': 92.9}, {'date': '2020-12-22', 'value': 87.1}, {'date': '2021-01-26', 'value': 88.9}, {'date': '2021-02-23', 'value': 90.4}, {'date': '2021-03-30', 'value': 109.0}, {'date': '2021-04-27', 'value': 117.5}, {'date': '2021-05-25', 'value': 120.0}, {'date': '2021-06-29', 'value': 128.9}, {'date': '2021-07-27', 'value': 125.1}, {'date': '2021-08-31', 'value': 115.2}, {'date': '2021-09-28', 'value': 109.8}, {'date': '2021-10-26', 'value': 111.6}, {'date': '2021-11-30', 'value': 111.9}, {'date': '2021-12-22', 'value': 115.2}, {'date': '2022-01-25', 'value': 111.1}, {'date': '2022-02-22', 'value': 105.7}, {'date': '2022-03-29', 'value': 107.6}, {'date': '2022-04-26', 'value': 108.6}, {'date': '2022-05-31', 'value': 103.2}, {'date': '2022-06-28', 'value': 98.4}, {'date': '2022-07-26', 'value': 95.3}, {'date': '2022-08-30', 'value': 103.6}, {'date': '2022-09-27', 'value': 107.8}, {'date': '2022-10-25', 'value': 102.2}, {'date': '2022-11-29', 'value': 101.4}, {'date': '2022-12-21', 'value': 109.0}, {'date': '2023-01-31', 'value': 106.0}, {'date': '2023-02-28', 'value': 103.4}, {'date': '2023-03-28', 'value': 104.0}, {'date': '2023-04-25', 'value': 103.7}, {'date': '2023-05-30', 'value': 102.5}, {'date': '2023-06-27', 'value': 110.1}, {'date': '2023-07-25', 'value': 114.0}, {'date': '2023-08-29', 'value': 108.7}, {'date': '2023-09-26', 'value': 104.3}, {'date': '2023-10-31', 'value': 99.1}, {'date': '2023-11-28', 'value': 101.0}, {'date': '2023-12-20', 'value': 108.0}, {'date': '2024-01-30', 'value': 110.9}, {'date': '2024-02-27', 'value': 104.8}, {'date': '2024-03-26', 'value': 103.1}, {'date': '2024-04-30', 'value': 97.5}, {'date': '2024-05-28', 'value': 102.0}]

    if exact_date:
        return data_series
    else:
        current_date = datetime.datetime.strptime('2008-01-01', '%Y-%m-%d')
        revised_data_series = []
        for x in data_series:
            current_date += pd.DateOffset(months=1)
            revised_data_series.append({
                'date': current_date.strftime('%Y-%m'),
                'value': x['value']
            })
        return revised_data_series

@st.cache_data
def get_civiqs_sentiment_data():

    print('Not cached - Civiqs sentiment data')

    sentiment = requests.get('https://results-api.civiqs.com/results_api/results/economy_us_now/trendline/%7B%7D?run_id=cf852969', headers={
        'Accept': 'application/vnd.questionator.v3',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }).json()
    
    list_data = []
    for entry, values in sentiment['trendline'].items():
        list_data.append({
            'date': datetime.datetime.utcfromtimestamp(int(entry)/1000).strftime('%Y-%m-%d'),
            'value': values['Very good'] + values['Fairly good'] - values['Fairly bad'] - values['Very bad']
        })

    return list_data

@st.cache_data
def get_civiqs_biden_job_approval_data():

    print('Not cached - Civiqs Biden approval data')

    sentiment = requests.get('https://results-api.civiqs.com/results_api/results/approve_president_biden/trendline/%7B%7D?run_id=293c6aed', headers={
        'Accept': 'application/vnd.questionator.v3',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }).json()
    
    list_data = []
    for entry, values in sentiment['trendline'].items():
        list_data.append({
            'date': datetime.datetime.utcfromtimestamp(int(entry)/1000).strftime('%Y-%m-%d'),
            'value': values['Approve'] - values['Disapprove']
        })

    return list_data

@st.cache_data
def get_democrat_in_white_house_data(start_date='1961-01-20'):

    print('Not cached - Dem in WH data')

    dem_in_white_house = [
        {
            'start_date': datetime.datetime.strptime('1961-01-20', '%Y-%m-%d').date(),
            'end_date': datetime.datetime.strptime('1969-01-19', '%Y-%m-%d').date()
        },
        {
            'start_date': datetime.datetime.strptime('1977-01-20', '%Y-%m-%d').date(),
            'end_date': datetime.datetime.strptime('1981-01-19', '%Y-%m-%d').date()
        },
        {
            'start_date': datetime.datetime.strptime('1993-01-20', '%Y-%m-%d').date(),
            'end_date': datetime.datetime.strptime('2001-01-19', '%Y-%m-%d').date()
        },
        {
            'start_date': datetime.datetime.strptime('2009-01-20', '%Y-%m-%d').date(),
            'end_date': datetime.datetime.strptime('2017-01-19', '%Y-%m-%d').date()
        },
        {
            'start_date': datetime.datetime.strptime('2021-01-20', '%Y-%m-%d').date()
        }
    ]

    start_date_as_date = max(datetime.datetime.strptime(start_date, '%Y-%m-%d').date(), datetime.datetime.strptime('1961-01-20', '%Y-%m-%d').date())
    list_data = []
    while start_date_as_date <= datetime.datetime.today().date():
        list_data.append({
            'date': start_date_as_date.strftime('%Y-%m-%d'),
            'value': next((1 for x in dem_in_white_house if x['start_date'] <= start_date_as_date and ('end_date' not in x or x['end_date'] >= start_date_as_date)), 0)
        })
        start_date_as_date += datetime.timedelta(days=1)

    return list_data

@st.cache_data
def get_frb_news_sentiment_data():

    print('Not cached - FRB news sentiment data')

    df = pd.read_excel('https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx?20240105', sheet_name='Data', names=['date', 'News Sentiment'])
    df = df.rename(columns={'News Sentiment': 'value'})
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    return df.to_dict(orient='records')

@st.cache_data
def get_gasbuddy_prices():

    print('Not cached - GasBuddy data')

    gas_prices = requests.post('https://fuelinsights.gasbuddy.com/api/HighChart/GetHighChartRecords/', json={
        "regionID":[500000],
        "fuelType":3,
        "timeWindow":[13],
        "frequency":1
    }).json()
    
    return [ {'date': datetime.datetime.strptime(x['datetime'], '%m/%d/%Y').strftime('%Y-%m-%d'), 'value': x['price']} for x in gas_prices[0]['USList']]

@st.cache_data
def get_joe_biden_polling_average():

    print('Not cached - 538 Biden polling data')

    polling_average = requests.get('https://projects.fivethirtyeight.com/polls/president-general/2024/national/polling-average.json').json()

    polling_average = [x for x in polling_average if x['candidate'] == 'Biden']

    polling_average = [ {(key if key == 'date' else 'value'): value for key, value in nested_dict.items() if key in ['date', 'pct_estimate']} for nested_dict in polling_average ]

    polling_average = sorted(polling_average, key = lambda x: x['date'])

    return polling_average

# Have to use a US IP (VPN)
@st.cache_data
def get_bls_data(series='inflation'):

    print('Not cached - BLS data')

    api_max_year_pagination = 10

    if series == 'inflation':
        start_year = 1913
        series_key = 'CUUR0000SA0'
    elif series == 'employment':
        start_year = 1939
        series_key = 'CES0000000001'
    elif series == 'unemployment':
        start_year = 1948
        series_key = 'LNS14000000'
    elif series == 'food_inflation':
        start_year = 1947
        series_key = 'CUSR0000SAF1'

    end_year = int(datetime.datetime.today().strftime('%Y'))
    headers = {
        'Content-type': 'application/json',
        'registrationkey': os.environ.get('BLS_API_KEY'),
        "catalog": 'false',
        "calculations": 'false',
        "annualaverage": 'false',
        "aspects": 'false'
    }

    list_data = []
    while start_year <= end_year:

        print(f"Processing years {start_year} - {min(start_year+api_max_year_pagination-1, end_year)}")

        data = {"seriesid": [series_key], "startyear": start_year, "endyear": min(start_year+api_max_year_pagination-1, end_year)} # BLS API V2 only allows pulling 10 (or 20? seems unclear, based on my usage/experience) years at a time

        json_data = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', json=data, headers=headers).json()

        print(json_data)
        list_data += json_data['Results']['series'][0]['data']
        start_year += api_max_year_pagination
    
    return sorted([ {'date': f"{x['year']}-{x['period'].split('M')[-1]}", 'value': float(x['value'])} for x in list_data], key=lambda x: x['date'])

@st.cache_data
def get_bls_inflation_data_statically():

    print('Not cached - BLS data')
    # See https://data.bls.gov/timeseries/CUUR0000SA0

    return [{'date': '1913-01', 'value': 9.8}, {'date': '1913-02', 'value': 9.8}, {'date': '1913-03', 'value': 9.8}, {'date': '1913-04', 'value': 9.8}, {'date': '1913-05', 'value': 9.7}, {'date': '1913-06', 'value': 9.8}, {'date': '1913-07', 'value': 9.9}, {'date': '1913-08', 'value': 9.9}, {'date': '1913-09', 'value': 10.0}, {'date': '1913-10', 'value': 10.0}, {'date': '1913-11', 'value': 10.1}, {'date': '1913-12', 'value': 10.0}, {'date': '1914-01', 'value': 10.0}, {'date': '1914-02', 'value': 9.9}, {'date': '1914-03', 'value': 9.9}, {'date': '1914-04', 'value': 9.8}, {'date': '1914-05', 'value': 9.9}, {'date': '1914-06', 'value': 9.9}, {'date': '1914-07', 'value': 10.0}, {'date': '1914-08', 'value': 10.2}, {'date': '1914-09', 'value': 10.2}, {'date': '1914-10', 'value': 10.1}, {'date': '1914-11', 'value': 10.2}, {'date': '1914-12', 'value': 10.1}, {'date': '1915-01', 'value': 10.1}, {'date': '1915-02', 'value': 10.0}, {'date': '1915-03', 'value': 9.9}, {'date': '1915-04', 'value': 10.0}, {'date': '1915-05', 'value': 10.1}, {'date': '1915-06', 'value': 10.1}, {'date': '1915-07', 'value': 10.1}, {'date': '1915-08', 'value': 10.1}, {'date': '1915-09', 'value': 10.1}, {'date': '1915-10', 'value': 10.2}, {'date': '1915-11', 'value': 10.3}, {'date': '1915-12', 'value': 10.3}, {'date': '1916-01', 'value': 10.4}, {'date': '1916-02', 'value': 10.4}, {'date': '1916-03', 'value': 10.5}, {'date': '1916-04', 'value': 10.6}, {'date': '1916-05', 'value': 10.7}, {'date': '1916-06', 'value': 10.8}, {'date': '1916-07', 'value': 10.8}, {'date': '1916-08', 'value': 10.9}, {'date': '1916-09', 'value': 11.1}, {'date': '1916-10', 'value': 11.3}, {'date': '1916-11', 'value': 11.5}, {'date': '1916-12', 'value': 11.6}, {'date': '1917-01', 'value': 11.7}, {'date': '1917-02', 'value': 12.0}, {'date': '1917-03', 'value': 12.0}, {'date': '1917-04', 'value': 12.6}, {'date': '1917-05', 'value': 12.8}, {'date': '1917-06', 'value': 13.0}, {'date': '1917-07', 'value': 12.8}, {'date': '1917-08', 'value': 13.0}, {'date': '1917-09', 'value': 13.3}, {'date': '1917-10', 'value': 13.5}, {'date': '1917-11', 'value': 13.5}, {'date': '1917-12', 'value': 13.7}, {'date': '1918-01', 'value': 14.0}, {'date': '1918-02', 'value': 14.1}, {'date': '1918-03', 'value': 14.0}, {'date': '1918-04', 'value': 14.2}, {'date': '1918-05', 'value': 14.5}, {'date': '1918-06', 'value': 14.7}, {'date': '1918-07', 'value': 15.1}, {'date': '1918-08', 'value': 15.4}, {'date': '1918-09', 'value': 15.7}, {'date': '1918-10', 'value': 16.0}, {'date': '1918-11', 'value': 16.3}, {'date': '1918-12', 'value': 16.5}, {'date': '1919-01', 'value': 16.5}, {'date': '1919-02', 'value': 16.2}, {'date': '1919-03', 'value': 16.4}, {'date': '1919-04', 'value': 16.7}, {'date': '1919-05', 'value': 16.9}, {'date': '1919-06', 'value': 16.9}, {'date': '1919-07', 'value': 17.4}, {'date': '1919-08', 'value': 17.7}, {'date': '1919-09', 'value': 17.8}, {'date': '1919-10', 'value': 18.1}, {'date': '1919-11', 'value': 18.5}, {'date': '1919-12', 'value': 18.9}, {'date': '1920-01', 'value': 19.3}, {'date': '1920-02', 'value': 19.5}, {'date': '1920-03', 'value': 19.7}, {'date': '1920-04', 'value': 20.3}, {'date': '1920-05', 'value': 20.6}, {'date': '1920-06', 'value': 20.9}, {'date': '1920-07', 'value': 20.8}, {'date': '1920-08', 'value': 20.3}, {'date': '1920-09', 'value': 20.0}, {'date': '1920-10', 'value': 19.9}, {'date': '1920-11', 'value': 19.8}, {'date': '1920-12', 'value': 19.4}, {'date': '1921-01', 'value': 19.0}, {'date': '1921-02', 'value': 18.4}, {'date': '1921-03', 'value': 18.3}, {'date': '1921-04', 'value': 18.1}, {'date': '1921-05', 'value': 17.7}, {'date': '1921-06', 'value': 17.6}, {'date': '1921-07', 'value': 17.7}, {'date': '1921-08', 'value': 17.7}, {'date': '1921-09', 'value': 17.5}, {'date': '1921-10', 'value': 17.5}, {'date': '1921-11', 'value': 17.4}, {'date': '1921-12', 'value': 17.3}, {'date': '1922-01', 'value': 16.9}, {'date': '1922-02', 'value': 16.9}, {'date': '1922-03', 'value': 16.7}, {'date': '1922-04', 'value': 16.7}, {'date': '1922-05', 'value': 16.7}, {'date': '1922-06', 'value': 16.7}, {'date': '1922-07', 'value': 16.8}, {'date': '1922-08', 'value': 16.6}, {'date': '1922-09', 'value': 16.6}, {'date': '1922-10', 'value': 16.7}, {'date': '1922-11', 'value': 16.8}, {'date': '1922-12', 'value': 16.9}, {'date': '1923-01', 'value': 16.8}, {'date': '1923-02', 'value': 16.8}, {'date': '1923-03', 'value': 16.8}, {'date': '1923-04', 'value': 16.9}, {'date': '1923-05', 'value': 16.9}, {'date': '1923-06', 'value': 17.0}, {'date': '1923-07', 'value': 17.2}, {'date': '1923-08', 'value': 17.1}, {'date': '1923-09', 'value': 17.2}, {'date': '1923-10', 'value': 17.3}, {'date': '1923-11', 'value': 17.3}, {'date': '1923-12', 'value': 17.3}, {'date': '1924-01', 'value': 17.3}, {'date': '1924-02', 'value': 17.2}, {'date': '1924-03', 'value': 17.1}, {'date': '1924-04', 'value': 17.0}, {'date': '1924-05', 'value': 17.0}, {'date': '1924-06', 'value': 17.0}, {'date': '1924-07', 'value': 17.1}, {'date': '1924-08', 'value': 17.0}, {'date': '1924-09', 'value': 17.1}, {'date': '1924-10', 'value': 17.2}, {'date': '1924-11', 'value': 17.2}, {'date': '1924-12', 'value': 17.3}, {'date': '1925-01', 'value': 17.3}, {'date': '1925-02', 'value': 17.2}, {'date': '1925-03', 'value': 17.3}, {'date': '1925-04', 'value': 17.2}, {'date': '1925-05', 'value': 17.3}, {'date': '1925-06', 'value': 17.5}, {'date': '1925-07', 'value': 17.7}, {'date': '1925-08', 'value': 17.7}, {'date': '1925-09', 'value': 17.7}, {'date': '1925-10', 'value': 17.7}, {'date': '1925-11', 'value': 18.0}, {'date': '1925-12', 'value': 17.9}, {'date': '1926-01', 'value': 17.9}, {'date': '1926-02', 'value': 17.9}, {'date': '1926-03', 'value': 17.8}, {'date': '1926-04', 'value': 17.9}, {'date': '1926-05', 'value': 17.8}, {'date': '1926-06', 'value': 17.7}, {'date': '1926-07', 'value': 17.5}, {'date': '1926-08', 'value': 17.4}, {'date': '1926-09', 'value': 17.5}, {'date': '1926-10', 'value': 17.6}, {'date': '1926-11', 'value': 17.7}, {'date': '1926-12', 'value': 17.7}, {'date': '1927-01', 'value': 17.5}, {'date': '1927-02', 'value': 17.4}, {'date': '1927-03', 'value': 17.3}, {'date': '1927-04', 'value': 17.3}, {'date': '1927-05', 'value': 17.4}, {'date': '1927-06', 'value': 17.6}, {'date': '1927-07', 'value': 17.3}, {'date': '1927-08', 'value': 17.2}, {'date': '1927-09', 'value': 17.3}, {'date': '1927-10', 'value': 17.4}, {'date': '1927-11', 'value': 17.3}, {'date': '1927-12', 'value': 17.3}, {'date': '1928-01', 'value': 17.3}, {'date': '1928-02', 'value': 17.1}, {'date': '1928-03', 'value': 17.1}, {'date': '1928-04', 'value': 17.1}, {'date': '1928-05', 'value': 17.2}, {'date': '1928-06', 'value': 17.1}, {'date': '1928-07', 'value': 17.1}, {'date': '1928-08', 'value': 17.1}, {'date': '1928-09', 'value': 17.3}, {'date': '1928-10', 'value': 17.2}, {'date': '1928-11', 'value': 17.2}, {'date': '1928-12', 'value': 17.1}, {'date': '1929-01', 'value': 17.1}, {'date': '1929-02', 'value': 17.1}, {'date': '1929-03', 'value': 17.0}, {'date': '1929-04', 'value': 16.9}, {'date': '1929-05', 'value': 17.0}, {'date': '1929-06', 'value': 17.1}, {'date': '1929-07', 'value': 17.3}, {'date': '1929-08', 'value': 17.3}, {'date': '1929-09', 'value': 17.3}, {'date': '1929-10', 'value': 17.3}, {'date': '1929-11', 'value': 17.3}, {'date': '1929-12', 'value': 17.2}, {'date': '1930-01', 'value': 17.1}, {'date': '1930-02', 'value': 17.0}, {'date': '1930-03', 'value': 16.9}, {'date': '1930-04', 'value': 17.0}, {'date': '1930-05', 'value': 16.9}, {'date': '1930-06', 'value': 16.8}, {'date': '1930-07', 'value': 16.6}, {'date': '1930-08', 'value': 16.5}, {'date': '1930-09', 'value': 16.6}, {'date': '1930-10', 'value': 16.5}, {'date': '1930-11', 'value': 16.4}, {'date': '1930-12', 'value': 16.1}, {'date': '1931-01', 'value': 15.9}, {'date': '1931-02', 'value': 15.7}, {'date': '1931-03', 'value': 15.6}, {'date': '1931-04', 'value': 15.5}, {'date': '1931-05', 'value': 15.3}, {'date': '1931-06', 'value': 15.1}, {'date': '1931-07', 'value': 15.1}, {'date': '1931-08', 'value': 15.1}, {'date': '1931-09', 'value': 15.0}, {'date': '1931-10', 'value': 14.9}, {'date': '1931-11', 'value': 14.7}, {'date': '1931-12', 'value': 14.6}, {'date': '1932-01', 'value': 14.3}, {'date': '1932-02', 'value': 14.1}, {'date': '1932-03', 'value': 14.0}, {'date': '1932-04', 'value': 13.9}, {'date': '1932-05', 'value': 13.7}, {'date': '1932-06', 'value': 13.6}, {'date': '1932-07', 'value': 13.6}, {'date': '1932-08', 'value': 13.5}, {'date': '1932-09', 'value': 13.4}, {'date': '1932-10', 'value': 13.3}, {'date': '1932-11', 'value': 13.2}, {'date': '1932-12', 'value': 13.1}, {'date': '1933-01', 'value': 12.9}, {'date': '1933-02', 'value': 12.7}, {'date': '1933-03', 'value': 12.6}, {'date': '1933-04', 'value': 12.6}, {'date': '1933-05', 'value': 12.6}, {'date': '1933-06', 'value': 12.7}, {'date': '1933-07', 'value': 13.1}, {'date': '1933-08', 'value': 13.2}, {'date': '1933-09', 'value': 13.2}, {'date': '1933-10', 'value': 13.2}, {'date': '1933-11', 'value': 13.2}, {'date': '1933-12', 'value': 13.2}, {'date': '1934-01', 'value': 13.2}, {'date': '1934-02', 'value': 13.3}, {'date': '1934-03', 'value': 13.3}, {'date': '1934-04', 'value': 13.3}, {'date': '1934-05', 'value': 13.3}, {'date': '1934-06', 'value': 13.4}, {'date': '1934-07', 'value': 13.4}, {'date': '1934-08', 'value': 13.4}, {'date': '1934-09', 'value': 13.6}, {'date': '1934-10', 'value': 13.5}, {'date': '1934-11', 'value': 13.5}, {'date': '1934-12', 'value': 13.4}, {'date': '1935-01', 'value': 13.6}, {'date': '1935-02', 'value': 13.7}, {'date': '1935-03', 'value': 13.7}, {'date': '1935-04', 'value': 13.8}, {'date': '1935-05', 'value': 13.8}, {'date': '1935-06', 'value': 13.7}, {'date': '1935-07', 'value': 13.7}, {'date': '1935-08', 'value': 13.7}, {'date': '1935-09', 'value': 13.7}, {'date': '1935-10', 'value': 13.7}, {'date': '1935-11', 'value': 13.8}, {'date': '1935-12', 'value': 13.8}, {'date': '1936-01', 'value': 13.8}, {'date': '1936-02', 'value': 13.8}, {'date': '1936-03', 'value': 13.7}, {'date': '1936-04', 'value': 13.7}, {'date': '1936-05', 'value': 13.7}, {'date': '1936-06', 'value': 13.8}, {'date': '1936-07', 'value': 13.9}, {'date': '1936-08', 'value': 14.0}, {'date': '1936-09', 'value': 14.0}, {'date': '1936-10', 'value': 14.0}, {'date': '1936-11', 'value': 14.0}, {'date': '1936-12', 'value': 14.0}, {'date': '1937-01', 'value': 14.1}, {'date': '1937-02', 'value': 14.1}, {'date': '1937-03', 'value': 14.2}, {'date': '1937-04', 'value': 14.3}, {'date': '1937-05', 'value': 14.4}, {'date': '1937-06', 'value': 14.4}, {'date': '1937-07', 'value': 14.5}, {'date': '1937-08', 'value': 14.5}, {'date': '1937-09', 'value': 14.6}, {'date': '1937-10', 'value': 14.6}, {'date': '1937-11', 'value': 14.5}, {'date': '1937-12', 'value': 14.4}, {'date': '1938-01', 'value': 14.2}, {'date': '1938-02', 'value': 14.1}, {'date': '1938-03', 'value': 14.1}, {'date': '1938-04', 'value': 14.2}, {'date': '1938-05', 'value': 14.1}, {'date': '1938-06', 'value': 14.1}, {'date': '1938-07', 'value': 14.1}, {'date': '1938-08', 'value': 14.1}, {'date': '1938-09', 'value': 14.1}, {'date': '1938-10', 'value': 14.0}, {'date': '1938-11', 'value': 14.0}, {'date': '1938-12', 'value': 14.0}, {'date': '1939-01', 'value': 14.0}, {'date': '1939-02', 'value': 13.9}, {'date': '1939-03', 'value': 13.9}, {'date': '1939-04', 'value': 13.8}, {'date': '1939-05', 'value': 13.8}, {'date': '1939-06', 'value': 13.8}, {'date': '1939-07', 'value': 13.8}, {'date': '1939-08', 'value': 13.8}, {'date': '1939-09', 'value': 14.1}, {'date': '1939-10', 'value': 14.0}, {'date': '1939-11', 'value': 14.0}, {'date': '1939-12', 'value': 14.0}, {'date': '1940-01', 'value': 13.9}, {'date': '1940-02', 'value': 14.0}, {'date': '1940-03', 'value': 14.0}, {'date': '1940-04', 'value': 14.0}, {'date': '1940-05', 'value': 14.0}, {'date': '1940-06', 'value': 14.1}, {'date': '1940-07', 'value': 14.0}, {'date': '1940-08', 'value': 14.0}, {'date': '1940-09', 'value': 14.0}, {'date': '1940-10', 'value': 14.0}, {'date': '1940-11', 'value': 14.0}, {'date': '1940-12', 'value': 14.1}, {'date': '1941-01', 'value': 14.1}, {'date': '1941-02', 'value': 14.1}, {'date': '1941-03', 'value': 14.2}, {'date': '1941-04', 'value': 14.3}, {'date': '1941-05', 'value': 14.4}, {'date': '1941-06', 'value': 14.7}, {'date': '1941-07', 'value': 14.7}, {'date': '1941-08', 'value': 14.9}, {'date': '1941-09', 'value': 15.1}, {'date': '1941-10', 'value': 15.3}, {'date': '1941-11', 'value': 15.4}, {'date': '1941-12', 'value': 15.5}, {'date': '1942-01', 'value': 15.7}, {'date': '1942-02', 'value': 15.8}, {'date': '1942-03', 'value': 16.0}, {'date': '1942-04', 'value': 16.1}, {'date': '1942-05', 'value': 16.3}, {'date': '1942-06', 'value': 16.3}, {'date': '1942-07', 'value': 16.4}, {'date': '1942-08', 'value': 16.5}, {'date': '1942-09', 'value': 16.5}, {'date': '1942-10', 'value': 16.7}, {'date': '1942-11', 'value': 16.8}, {'date': '1942-12', 'value': 16.9}, {'date': '1943-01', 'value': 16.9}, {'date': '1943-02', 'value': 16.9}, {'date': '1943-03', 'value': 17.2}, {'date': '1943-04', 'value': 17.4}, {'date': '1943-05', 'value': 17.5}, {'date': '1943-06', 'value': 17.5}, {'date': '1943-07', 'value': 17.4}, {'date': '1943-08', 'value': 17.3}, {'date': '1943-09', 'value': 17.4}, {'date': '1943-10', 'value': 17.4}, {'date': '1943-11', 'value': 17.4}, {'date': '1943-12', 'value': 17.4}, {'date': '1944-01', 'value': 17.4}, {'date': '1944-02', 'value': 17.4}, {'date': '1944-03', 'value': 17.4}, {'date': '1944-04', 'value': 17.5}, {'date': '1944-05', 'value': 17.5}, {'date': '1944-06', 'value': 17.6}, {'date': '1944-07', 'value': 17.7}, {'date': '1944-08', 'value': 17.7}, {'date': '1944-09', 'value': 17.7}, {'date': '1944-10', 'value': 17.7}, {'date': '1944-11', 'value': 17.7}, {'date': '1944-12', 'value': 17.8}, {'date': '1945-01', 'value': 17.8}, {'date': '1945-02', 'value': 17.8}, {'date': '1945-03', 'value': 17.8}, {'date': '1945-04', 'value': 17.8}, {'date': '1945-05', 'value': 17.9}, {'date': '1945-06', 'value': 18.1}, {'date': '1945-07', 'value': 18.1}, {'date': '1945-08', 'value': 18.1}, {'date': '1945-09', 'value': 18.1}, {'date': '1945-10', 'value': 18.1}, {'date': '1945-11', 'value': 18.1}, {'date': '1945-12', 'value': 18.2}, {'date': '1946-01', 'value': 18.2}, {'date': '1946-02', 'value': 18.1}, {'date': '1946-03', 'value': 18.3}, {'date': '1946-04', 'value': 18.4}, {'date': '1946-05', 'value': 18.5}, {'date': '1946-06', 'value': 18.7}, {'date': '1946-07', 'value': 19.8}, {'date': '1946-08', 'value': 20.2}, {'date': '1946-09', 'value': 20.4}, {'date': '1946-10', 'value': 20.8}, {'date': '1946-11', 'value': 21.3}, {'date': '1946-12', 'value': 21.5}, {'date': '1947-01', 'value': 21.5}, {'date': '1947-02', 'value': 21.5}, {'date': '1947-03', 'value': 21.9}, {'date': '1947-04', 'value': 21.9}, {'date': '1947-05', 'value': 21.9}, {'date': '1947-06', 'value': 22.0}, {'date': '1947-07', 'value': 22.2}, {'date': '1947-08', 'value': 22.5}, {'date': '1947-09', 'value': 23.0}, {'date': '1947-10', 'value': 23.0}, {'date': '1947-11', 'value': 23.1}, {'date': '1947-12', 'value': 23.4}, {'date': '1948-01', 'value': 23.7}, {'date': '1948-02', 'value': 23.5}, {'date': '1948-03', 'value': 23.4}, {'date': '1948-04', 'value': 23.8}, {'date': '1948-05', 'value': 23.9}, {'date': '1948-06', 'value': 24.1}, {'date': '1948-07', 'value': 24.4}, {'date': '1948-08', 'value': 24.5}, {'date': '1948-09', 'value': 24.5}, {'date': '1948-10', 'value': 24.4}, {'date': '1948-11', 'value': 24.2}, {'date': '1948-12', 'value': 24.1}, {'date': '1949-01', 'value': 24.0}, {'date': '1949-02', 'value': 23.8}, {'date': '1949-03', 'value': 23.8}, {'date': '1949-04', 'value': 23.9}, {'date': '1949-05', 'value': 23.8}, {'date': '1949-06', 'value': 23.9}, {'date': '1949-07', 'value': 23.7}, {'date': '1949-08', 'value': 23.8}, {'date': '1949-09', 'value': 23.9}, {'date': '1949-10', 'value': 23.7}, {'date': '1949-11', 'value': 23.8}, {'date': '1949-12', 'value': 23.6}, {'date': '1950-01', 'value': 23.5}, {'date': '1950-02', 'value': 23.5}, {'date': '1950-03', 'value': 23.6}, {'date': '1950-04', 'value': 23.6}, {'date': '1950-05', 'value': 23.7}, {'date': '1950-06', 'value': 23.8}, {'date': '1950-07', 'value': 24.1}, {'date': '1950-08', 'value': 24.3}, {'date': '1950-09', 'value': 24.4}, {'date': '1950-10', 'value': 24.6}, {'date': '1950-11', 'value': 24.7}, {'date': '1950-12', 'value': 25.0}, {'date': '1951-01', 'value': 25.4}, {'date': '1951-02', 'value': 25.7}, {'date': '1951-03', 'value': 25.8}, {'date': '1951-04', 'value': 25.8}, {'date': '1951-05', 'value': 25.9}, {'date': '1951-06', 'value': 25.9}, {'date': '1951-07', 'value': 25.9}, {'date': '1951-08', 'value': 25.9}, {'date': '1951-09', 'value': 26.1}, {'date': '1951-10', 'value': 26.2}, {'date': '1951-11', 'value': 26.4}, {'date': '1951-12', 'value': 26.5}, {'date': '1952-01', 'value': 26.5}, {'date': '1952-02', 'value': 26.3}, {'date': '1952-03', 'value': 26.3}, {'date': '1952-04', 'value': 26.4}, {'date': '1952-05', 'value': 26.4}, {'date': '1952-06', 'value': 26.5}, {'date': '1952-07', 'value': 26.7}, {'date': '1952-08', 'value': 26.7}, {'date': '1952-09', 'value': 26.7}, {'date': '1952-10', 'value': 26.7}, {'date': '1952-11', 'value': 26.7}, {'date': '1952-12', 'value': 26.7}, {'date': '1953-01', 'value': 26.6}, {'date': '1953-02', 'value': 26.5}, {'date': '1953-03', 'value': 26.6}, {'date': '1953-04', 'value': 26.6}, {'date': '1953-05', 'value': 26.7}, {'date': '1953-06', 'value': 26.8}, {'date': '1953-07', 'value': 26.8}, {'date': '1953-08', 'value': 26.9}, {'date': '1953-09', 'value': 26.9}, {'date': '1953-10', 'value': 27.0}, {'date': '1953-11', 'value': 26.9}, {'date': '1953-12', 'value': 26.9}, {'date': '1954-01', 'value': 26.9}, {'date': '1954-02', 'value': 26.9}, {'date': '1954-03', 'value': 26.9}, {'date': '1954-04', 'value': 26.8}, {'date': '1954-05', 'value': 26.9}, {'date': '1954-06', 'value': 26.9}, {'date': '1954-07', 'value': 26.9}, {'date': '1954-08', 'value': 26.9}, {'date': '1954-09', 'value': 26.8}, {'date': '1954-10', 'value': 26.8}, {'date': '1954-11', 'value': 26.8}, {'date': '1954-12', 'value': 26.7}, {'date': '1955-01', 'value': 26.7}, {'date': '1955-02', 'value': 26.7}, {'date': '1955-03', 'value': 26.7}, {'date': '1955-04', 'value': 26.7}, {'date': '1955-05', 'value': 26.7}, {'date': '1955-06', 'value': 26.7}, {'date': '1955-07', 'value': 26.8}, {'date': '1955-08', 'value': 26.8}, {'date': '1955-09', 'value': 26.9}, {'date': '1955-10', 'value': 26.9}, {'date': '1955-11', 'value': 26.9}, {'date': '1955-12', 'value': 26.8}, {'date': '1956-01', 'value': 26.8}, {'date': '1956-02', 'value': 26.8}, {'date': '1956-03', 'value': 26.8}, {'date': '1956-04', 'value': 26.9}, {'date': '1956-05', 'value': 27.0}, {'date': '1956-06', 'value': 27.2}, {'date': '1956-07', 'value': 27.4}, {'date': '1956-08', 'value': 27.3}, {'date': '1956-09', 'value': 27.4}, {'date': '1956-10', 'value': 27.5}, {'date': '1956-11', 'value': 27.5}, {'date': '1956-12', 'value': 27.6}, {'date': '1957-01', 'value': 27.6}, {'date': '1957-02', 'value': 27.7}, {'date': '1957-03', 'value': 27.8}, {'date': '1957-04', 'value': 27.9}, {'date': '1957-05', 'value': 28.0}, {'date': '1957-06', 'value': 28.1}, {'date': '1957-07', 'value': 28.3}, {'date': '1957-08', 'value': 28.3}, {'date': '1957-09', 'value': 28.3}, {'date': '1957-10', 'value': 28.3}, {'date': '1957-11', 'value': 28.4}, {'date': '1957-12', 'value': 28.4}, {'date': '1958-01', 'value': 28.6}, {'date': '1958-02', 'value': 28.6}, {'date': '1958-03', 'value': 28.8}, {'date': '1958-04', 'value': 28.9}, {'date': '1958-05', 'value': 28.9}, {'date': '1958-06', 'value': 28.9}, {'date': '1958-07', 'value': 29.0}, {'date': '1958-08', 'value': 28.9}, {'date': '1958-09', 'value': 28.9}, {'date': '1958-10', 'value': 28.9}, {'date': '1958-11', 'value': 29.0}, {'date': '1958-12', 'value': 28.9}, {'date': '1959-01', 'value': 29.0}, {'date': '1959-02', 'value': 28.9}, {'date': '1959-03', 'value': 28.9}, {'date': '1959-04', 'value': 29.0}, {'date': '1959-05', 'value': 29.0}, {'date': '1959-06', 'value': 29.1}, {'date': '1959-07', 'value': 29.2}, {'date': '1959-08', 'value': 29.2}, {'date': '1959-09', 'value': 29.3}, {'date': '1959-10', 'value': 29.4}, {'date': '1959-11', 'value': 29.4}, {'date': '1959-12', 'value': 29.4}, {'date': '1960-01', 'value': 29.3}, {'date': '1960-02', 'value': 29.4}, {'date': '1960-03', 'value': 29.4}, {'date': '1960-04', 'value': 29.5}, {'date': '1960-05', 'value': 29.5}, {'date': '1960-06', 'value': 29.6}, {'date': '1960-07', 'value': 29.6}, {'date': '1960-08', 'value': 29.6}, {'date': '1960-09', 'value': 29.6}, {'date': '1960-10', 'value': 29.8}, {'date': '1960-11', 'value': 29.8}, {'date': '1960-12', 'value': 29.8}, {'date': '1961-01', 'value': 29.8}, {'date': '1961-02', 'value': 29.8}, {'date': '1961-03', 'value': 29.8}, {'date': '1961-04', 'value': 29.8}, {'date': '1961-05', 'value': 29.8}, {'date': '1961-06', 'value': 29.8}, {'date': '1961-07', 'value': 30.0}, {'date': '1961-08', 'value': 29.9}, {'date': '1961-09', 'value': 30.0}, {'date': '1961-10', 'value': 30.0}, {'date': '1961-11', 'value': 30.0}, {'date': '1961-12', 'value': 30.0}, {'date': '1962-01', 'value': 30.0}, {'date': '1962-02', 'value': 30.1}, {'date': '1962-03', 'value': 30.1}, {'date': '1962-04', 'value': 30.2}, {'date': '1962-05', 'value': 30.2}, {'date': '1962-06', 'value': 30.2}, {'date': '1962-07', 'value': 30.3}, {'date': '1962-08', 'value': 30.3}, {'date': '1962-09', 'value': 30.4}, {'date': '1962-10', 'value': 30.4}, {'date': '1962-11', 'value': 30.4}, {'date': '1962-12', 'value': 30.4}, {'date': '1963-01', 'value': 30.4}, {'date': '1963-02', 'value': 30.4}, {'date': '1963-03', 'value': 30.5}, {'date': '1963-04', 'value': 30.5}, {'date': '1963-05', 'value': 30.5}, {'date': '1963-06', 'value': 30.6}, {'date': '1963-07', 'value': 30.7}, {'date': '1963-08', 'value': 30.7}, {'date': '1963-09', 'value': 30.7}, {'date': '1963-10', 'value': 30.8}, {'date': '1963-11', 'value': 30.8}, {'date': '1963-12', 'value': 30.9}, {'date': '1964-01', 'value': 30.9}, {'date': '1964-02', 'value': 30.9}, {'date': '1964-03', 'value': 30.9}, {'date': '1964-04', 'value': 30.9}, {'date': '1964-05', 'value': 30.9}, {'date': '1964-06', 'value': 31.0}, {'date': '1964-07', 'value': 31.1}, {'date': '1964-08', 'value': 31.0}, {'date': '1964-09', 'value': 31.1}, {'date': '1964-10', 'value': 31.1}, {'date': '1964-11', 'value': 31.2}, {'date': '1964-12', 'value': 31.2}, {'date': '1965-01', 'value': 31.2}, {'date': '1965-02', 'value': 31.2}, {'date': '1965-03', 'value': 31.3}, {'date': '1965-04', 'value': 31.4}, {'date': '1965-05', 'value': 31.4}, {'date': '1965-06', 'value': 31.6}, {'date': '1965-07', 'value': 31.6}, {'date': '1965-08', 'value': 31.6}, {'date': '1965-09', 'value': 31.6}, {'date': '1965-10', 'value': 31.7}, {'date': '1965-11', 'value': 31.7}, {'date': '1965-12', 'value': 31.8}, {'date': '1966-01', 'value': 31.8}, {'date': '1966-02', 'value': 32.0}, {'date': '1966-03', 'value': 32.1}, {'date': '1966-04', 'value': 32.3}, {'date': '1966-05', 'value': 32.3}, {'date': '1966-06', 'value': 32.4}, {'date': '1966-07', 'value': 32.5}, {'date': '1966-08', 'value': 32.7}, {'date': '1966-09', 'value': 32.7}, {'date': '1966-10', 'value': 32.9}, {'date': '1966-11', 'value': 32.9}, {'date': '1966-12', 'value': 32.9}, {'date': '1967-01', 'value': 32.9}, {'date': '1967-02', 'value': 32.9}, {'date': '1967-03', 'value': 33.0}, {'date': '1967-04', 'value': 33.1}, {'date': '1967-05', 'value': 33.2}, {'date': '1967-06', 'value': 33.3}, {'date': '1967-07', 'value': 33.4}, {'date': '1967-08', 'value': 33.5}, {'date': '1967-09', 'value': 33.6}, {'date': '1967-10', 'value': 33.7}, {'date': '1967-11', 'value': 33.8}, {'date': '1967-12', 'value': 33.9}, {'date': '1968-01', 'value': 34.1}, {'date': '1968-02', 'value': 34.2}, {'date': '1968-03', 'value': 34.3}, {'date': '1968-04', 'value': 34.4}, {'date': '1968-05', 'value': 34.5}, {'date': '1968-06', 'value': 34.7}, {'date': '1968-07', 'value': 34.9}, {'date': '1968-08', 'value': 35.0}, {'date': '1968-09', 'value': 35.1}, {'date': '1968-10', 'value': 35.3}, {'date': '1968-11', 'value': 35.4}, {'date': '1968-12', 'value': 35.5}, {'date': '1969-01', 'value': 35.6}, {'date': '1969-02', 'value': 35.8}, {'date': '1969-03', 'value': 36.1}, {'date': '1969-04', 'value': 36.3}, {'date': '1969-05', 'value': 36.4}, {'date': '1969-06', 'value': 36.6}, {'date': '1969-07', 'value': 36.8}, {'date': '1969-08', 'value': 37.0}, {'date': '1969-09', 'value': 37.1}, {'date': '1969-10', 'value': 37.3}, {'date': '1969-11', 'value': 37.5}, {'date': '1969-12', 'value': 37.7}, {'date': '1970-01', 'value': 37.8}, {'date': '1970-02', 'value': 38.0}, {'date': '1970-03', 'value': 38.2}, {'date': '1970-04', 'value': 38.5}, {'date': '1970-05', 'value': 38.6}, {'date': '1970-06', 'value': 38.8}, {'date': '1970-07', 'value': 39.0}, {'date': '1970-08', 'value': 39.0}, {'date': '1970-09', 'value': 39.2}, {'date': '1970-10', 'value': 39.4}, {'date': '1970-11', 'value': 39.6}, {'date': '1970-12', 'value': 39.8}, {'date': '1971-01', 'value': 39.8}, {'date': '1971-02', 'value': 39.9}, {'date': '1971-03', 'value': 40.0}, {'date': '1971-04', 'value': 40.1}, {'date': '1971-05', 'value': 40.3}, {'date': '1971-06', 'value': 40.6}, {'date': '1971-07', 'value': 40.7}, {'date': '1971-08', 'value': 40.8}, {'date': '1971-09', 'value': 40.8}, {'date': '1971-10', 'value': 40.9}, {'date': '1971-11', 'value': 40.9}, {'date': '1971-12', 'value': 41.1}, {'date': '1972-01', 'value': 41.1}, {'date': '1972-02', 'value': 41.3}, {'date': '1972-03', 'value': 41.4}, {'date': '1972-04', 'value': 41.5}, {'date': '1972-05', 'value': 41.6}, {'date': '1972-06', 'value': 41.7}, {'date': '1972-07', 'value': 41.9}, {'date': '1972-08', 'value': 42.0}, {'date': '1972-09', 'value': 42.1}, {'date': '1972-10', 'value': 42.3}, {'date': '1972-11', 'value': 42.4}, {'date': '1972-12', 'value': 42.5}, {'date': '1973-01', 'value': 42.6}, {'date': '1973-02', 'value': 42.9}, {'date': '1973-03', 'value': 43.3}, {'date': '1973-04', 'value': 43.6}, {'date': '1973-05', 'value': 43.9}, {'date': '1973-06', 'value': 44.2}, {'date': '1973-07', 'value': 44.3}, {'date': '1973-08', 'value': 45.1}, {'date': '1973-09', 'value': 45.2}, {'date': '1973-10', 'value': 45.6}, {'date': '1973-11', 'value': 45.9}, {'date': '1973-12', 'value': 46.2}, {'date': '1974-01', 'value': 46.6}, {'date': '1974-02', 'value': 47.2}, {'date': '1974-03', 'value': 47.8}, {'date': '1974-04', 'value': 48.0}, {'date': '1974-05', 'value': 48.6}, {'date': '1974-06', 'value': 49.0}, {'date': '1974-07', 'value': 49.4}, {'date': '1974-08', 'value': 50.0}, {'date': '1974-09', 'value': 50.6}, {'date': '1974-10', 'value': 51.1}, {'date': '1974-11', 'value': 51.5}, {'date': '1974-12', 'value': 51.9}, {'date': '1975-01', 'value': 52.1}, {'date': '1975-02', 'value': 52.5}, {'date': '1975-03', 'value': 52.7}, {'date': '1975-04', 'value': 52.9}, {'date': '1975-05', 'value': 53.2}, {'date': '1975-06', 'value': 53.6}, {'date': '1975-07', 'value': 54.2}, {'date': '1975-08', 'value': 54.3}, {'date': '1975-09', 'value': 54.6}, {'date': '1975-10', 'value': 54.9}, {'date': '1975-11', 'value': 55.3}, {'date': '1975-12', 'value': 55.5}, {'date': '1976-01', 'value': 55.6}, {'date': '1976-02', 'value': 55.8}, {'date': '1976-03', 'value': 55.9}, {'date': '1976-04', 'value': 56.1}, {'date': '1976-05', 'value': 56.5}, {'date': '1976-06', 'value': 56.8}, {'date': '1976-07', 'value': 57.1}, {'date': '1976-08', 'value': 57.4}, {'date': '1976-09', 'value': 57.6}, {'date': '1976-10', 'value': 57.9}, {'date': '1976-11', 'value': 58.0}, {'date': '1976-12', 'value': 58.2}, {'date': '1977-01', 'value': 58.5}, {'date': '1977-02', 'value': 59.1}, {'date': '1977-03', 'value': 59.5}, {'date': '1977-04', 'value': 60.0}, {'date': '1977-05', 'value': 60.3}, {'date': '1977-06', 'value': 60.7}, {'date': '1977-07', 'value': 61.0}, {'date': '1977-08', 'value': 61.2}, {'date': '1977-09', 'value': 61.4}, {'date': '1977-10', 'value': 61.6}, {'date': '1977-11', 'value': 61.9}, {'date': '1977-12', 'value': 62.1}, {'date': '1978-01', 'value': 62.5}, {'date': '1978-02', 'value': 62.9}, {'date': '1978-03', 'value': 63.4}, {'date': '1978-04', 'value': 63.9}, {'date': '1978-05', 'value': 64.5}, {'date': '1978-06', 'value': 65.2}, {'date': '1978-07', 'value': 65.7}, {'date': '1978-08', 'value': 66.0}, {'date': '1978-09', 'value': 66.5}, {'date': '1978-10', 'value': 67.1}, {'date': '1978-11', 'value': 67.4}, {'date': '1978-12', 'value': 67.7}, {'date': '1979-01', 'value': 68.3}, {'date': '1979-02', 'value': 69.1}, {'date': '1979-03', 'value': 69.8}, {'date': '1979-04', 'value': 70.6}, {'date': '1979-05', 'value': 71.5}, {'date': '1979-06', 'value': 72.3}, {'date': '1979-07', 'value': 73.1}, {'date': '1979-08', 'value': 73.8}, {'date': '1979-09', 'value': 74.6}, {'date': '1979-10', 'value': 75.2}, {'date': '1979-11', 'value': 75.9}, {'date': '1979-12', 'value': 76.7}, {'date': '1980-01', 'value': 77.8}, {'date': '1980-02', 'value': 78.9}, {'date': '1980-03', 'value': 80.1}, {'date': '1980-04', 'value': 81.0}, {'date': '1980-05', 'value': 81.8}, {'date': '1980-06', 'value': 82.7}, {'date': '1980-07', 'value': 82.7}, {'date': '1980-08', 'value': 83.3}, {'date': '1980-09', 'value': 84.0}, {'date': '1980-10', 'value': 84.8}, {'date': '1980-11', 'value': 85.5}, {'date': '1980-12', 'value': 86.3}, {'date': '1981-01', 'value': 87.0}, {'date': '1981-02', 'value': 87.9}, {'date': '1981-03', 'value': 88.5}, {'date': '1981-04', 'value': 89.1}, {'date': '1981-05', 'value': 89.8}, {'date': '1981-06', 'value': 90.6}, {'date': '1981-07', 'value': 91.6}, {'date': '1981-08', 'value': 92.3}, {'date': '1981-09', 'value': 93.2}, {'date': '1981-10', 'value': 93.4}, {'date': '1981-11', 'value': 93.7}, {'date': '1981-12', 'value': 94.0}, {'date': '1982-01', 'value': 94.3}, {'date': '1982-02', 'value': 94.6}, {'date': '1982-03', 'value': 94.5}, {'date': '1982-04', 'value': 94.9}, {'date': '1982-05', 'value': 95.8}, {'date': '1982-06', 'value': 97.0}, {'date': '1982-07', 'value': 97.5}, {'date': '1982-08', 'value': 97.7}, {'date': '1982-09', 'value': 97.9}, {'date': '1982-10', 'value': 98.2}, {'date': '1982-11', 'value': 98.0}, {'date': '1982-12', 'value': 97.6}, {'date': '1983-01', 'value': 97.8}, {'date': '1983-02', 'value': 97.9}, {'date': '1983-03', 'value': 97.9}, {'date': '1983-04', 'value': 98.6}, {'date': '1983-05', 'value': 99.2}, {'date': '1983-06', 'value': 99.5}, {'date': '1983-07', 'value': 99.9}, {'date': '1983-08', 'value': 100.2}, {'date': '1983-09', 'value': 100.7}, {'date': '1983-10', 'value': 101.0}, {'date': '1983-11', 'value': 101.2}, {'date': '1983-12', 'value': 101.3}, {'date': '1984-01', 'value': 101.9}, {'date': '1984-02', 'value': 102.4}, {'date': '1984-03', 'value': 102.6}, {'date': '1984-04', 'value': 103.1}, {'date': '1984-05', 'value': 103.4}, {'date': '1984-06', 'value': 103.7}, {'date': '1984-07', 'value': 104.1}, {'date': '1984-08', 'value': 104.5}, {'date': '1984-09', 'value': 105.0}, {'date': '1984-10', 'value': 105.3}, {'date': '1984-11', 'value': 105.3}, {'date': '1984-12', 'value': 105.3}, {'date': '1985-01', 'value': 105.5}, {'date': '1985-02', 'value': 106.0}, {'date': '1985-03', 'value': 106.4}, {'date': '1985-04', 'value': 106.9}, {'date': '1985-05', 'value': 107.3}, {'date': '1985-06', 'value': 107.6}, {'date': '1985-07', 'value': 107.8}, {'date': '1985-08', 'value': 108.0}, {'date': '1985-09', 'value': 108.3}, {'date': '1985-10', 'value': 108.7}, {'date': '1985-11', 'value': 109.0}, {'date': '1985-12', 'value': 109.3}, {'date': '1986-01', 'value': 109.6}, {'date': '1986-02', 'value': 109.3}, {'date': '1986-03', 'value': 108.8}, {'date': '1986-04', 'value': 108.6}, {'date': '1986-05', 'value': 108.9}, {'date': '1986-06', 'value': 109.5}, {'date': '1986-07', 'value': 109.5}, {'date': '1986-08', 'value': 109.7}, {'date': '1986-09', 'value': 110.2}, {'date': '1986-10', 'value': 110.3}, {'date': '1986-11', 'value': 110.4}, {'date': '1986-12', 'value': 110.5}, {'date': '1987-01', 'value': 111.2}, {'date': '1987-02', 'value': 111.6}, {'date': '1987-03', 'value': 112.1}, {'date': '1987-04', 'value': 112.7}, {'date': '1987-05', 'value': 113.1}, {'date': '1987-06', 'value': 113.5}, {'date': '1987-07', 'value': 113.8}, {'date': '1987-08', 'value': 114.4}, {'date': '1987-09', 'value': 115.0}, {'date': '1987-10', 'value': 115.3}, {'date': '1987-11', 'value': 115.4}, {'date': '1987-12', 'value': 115.4}, {'date': '1988-01', 'value': 115.7}, {'date': '1988-02', 'value': 116.0}, {'date': '1988-03', 'value': 116.5}, {'date': '1988-04', 'value': 117.1}, {'date': '1988-05', 'value': 117.5}, {'date': '1988-06', 'value': 118.0}, {'date': '1988-07', 'value': 118.5}, {'date': '1988-08', 'value': 119.0}, {'date': '1988-09', 'value': 119.8}, {'date': '1988-10', 'value': 120.2}, {'date': '1988-11', 'value': 120.3}, {'date': '1988-12', 'value': 120.5}, {'date': '1989-01', 'value': 121.1}, {'date': '1989-02', 'value': 121.6}, {'date': '1989-03', 'value': 122.3}, {'date': '1989-04', 'value': 123.1}, {'date': '1989-05', 'value': 123.8}, {'date': '1989-06', 'value': 124.1}, {'date': '1989-07', 'value': 124.4}, {'date': '1989-08', 'value': 124.6}, {'date': '1989-09', 'value': 125.0}, {'date': '1989-10', 'value': 125.6}, {'date': '1989-11', 'value': 125.9}, {'date': '1989-12', 'value': 126.1}, {'date': '1990-01', 'value': 127.4}, {'date': '1990-02', 'value': 128.0}, {'date': '1990-03', 'value': 128.7}, {'date': '1990-04', 'value': 128.9}, {'date': '1990-05', 'value': 129.2}, {'date': '1990-06', 'value': 129.9}, {'date': '1990-07', 'value': 130.4}, {'date': '1990-08', 'value': 131.6}, {'date': '1990-09', 'value': 132.7}, {'date': '1990-10', 'value': 133.5}, {'date': '1990-11', 'value': 133.8}, {'date': '1990-12', 'value': 133.8}, {'date': '1991-01', 'value': 134.6}, {'date': '1991-02', 'value': 134.8}, {'date': '1991-03', 'value': 135.0}, {'date': '1991-04', 'value': 135.2}, {'date': '1991-05', 'value': 135.6}, {'date': '1991-06', 'value': 136.0}, {'date': '1991-07', 'value': 136.2}, {'date': '1991-08', 'value': 136.6}, {'date': '1991-09', 'value': 137.2}, {'date': '1991-10', 'value': 137.4}, {'date': '1991-11', 'value': 137.8}, {'date': '1991-12', 'value': 137.9}, {'date': '1992-01', 'value': 138.1}, {'date': '1992-02', 'value': 138.6}, {'date': '1992-03', 'value': 139.3}, {'date': '1992-04', 'value': 139.5}, {'date': '1992-05', 'value': 139.7}, {'date': '1992-06', 'value': 140.2}, {'date': '1992-07', 'value': 140.5}, {'date': '1992-08', 'value': 140.9}, {'date': '1992-09', 'value': 141.3}, {'date': '1992-10', 'value': 141.8}, {'date': '1992-11', 'value': 142.0}, {'date': '1992-12', 'value': 141.9}, {'date': '1993-01', 'value': 142.6}, {'date': '1993-02', 'value': 143.1}, {'date': '1993-03', 'value': 143.6}, {'date': '1993-04', 'value': 144.0}, {'date': '1993-05', 'value': 144.2}, {'date': '1993-06', 'value': 144.4}, {'date': '1993-07', 'value': 144.4}, {'date': '1993-08', 'value': 144.8}, {'date': '1993-09', 'value': 145.1}, {'date': '1993-10', 'value': 145.7}, {'date': '1993-11', 'value': 145.8}, {'date': '1993-12', 'value': 145.8}, {'date': '1994-01', 'value': 146.2}, {'date': '1994-02', 'value': 146.7}, {'date': '1994-03', 'value': 147.2}, {'date': '1994-04', 'value': 147.4}, {'date': '1994-05', 'value': 147.5}, {'date': '1994-06', 'value': 148.0}, {'date': '1994-07', 'value': 148.4}, {'date': '1994-08', 'value': 149.0}, {'date': '1994-09', 'value': 149.4}, {'date': '1994-10', 'value': 149.5}, {'date': '1994-11', 'value': 149.7}, {'date': '1994-12', 'value': 149.7}, {'date': '1995-01', 'value': 150.3}, {'date': '1995-02', 'value': 150.9}, {'date': '1995-03', 'value': 151.4}, {'date': '1995-04', 'value': 151.9}, {'date': '1995-05', 'value': 152.2}, {'date': '1995-06', 'value': 152.5}, {'date': '1995-07', 'value': 152.5}, {'date': '1995-08', 'value': 152.9}, {'date': '1995-09', 'value': 153.2}, {'date': '1995-10', 'value': 153.7}, {'date': '1995-11', 'value': 153.6}, {'date': '1995-12', 'value': 153.5}, {'date': '1996-01', 'value': 154.4}, {'date': '1996-02', 'value': 154.9}, {'date': '1996-03', 'value': 155.7}, {'date': '1996-04', 'value': 156.3}, {'date': '1996-05', 'value': 156.6}, {'date': '1996-06', 'value': 156.7}, {'date': '1996-07', 'value': 157.0}, {'date': '1996-08', 'value': 157.3}, {'date': '1996-09', 'value': 157.8}, {'date': '1996-10', 'value': 158.3}, {'date': '1996-11', 'value': 158.6}, {'date': '1996-12', 'value': 158.6}, {'date': '1997-01', 'value': 159.1}, {'date': '1997-02', 'value': 159.6}, {'date': '1997-03', 'value': 160.0}, {'date': '1997-04', 'value': 160.2}, {'date': '1997-05', 'value': 160.1}, {'date': '1997-06', 'value': 160.3}, {'date': '1997-07', 'value': 160.5}, {'date': '1997-08', 'value': 160.8}, {'date': '1997-09', 'value': 161.2}, {'date': '1997-10', 'value': 161.6}, {'date': '1997-11', 'value': 161.5}, {'date': '1997-12', 'value': 161.3}, {'date': '1998-01', 'value': 161.6}, {'date': '1998-02', 'value': 161.9}, {'date': '1998-03', 'value': 162.2}, {'date': '1998-04', 'value': 162.5}, {'date': '1998-05', 'value': 162.8}, {'date': '1998-06', 'value': 163.0}, {'date': '1998-07', 'value': 163.2}, {'date': '1998-08', 'value': 163.4}, {'date': '1998-09', 'value': 163.6}, {'date': '1998-10', 'value': 164.0}, {'date': '1998-11', 'value': 164.0}, {'date': '1998-12', 'value': 163.9}, {'date': '1999-01', 'value': 164.3}, {'date': '1999-02', 'value': 164.5}, {'date': '1999-03', 'value': 165.0}, {'date': '1999-04', 'value': 166.2}, {'date': '1999-05', 'value': 166.2}, {'date': '1999-06', 'value': 166.2}, {'date': '1999-07', 'value': 166.7}, {'date': '1999-08', 'value': 167.1}, {'date': '1999-09', 'value': 167.9}, {'date': '1999-10', 'value': 168.2}, {'date': '1999-11', 'value': 168.3}, {'date': '1999-12', 'value': 168.3}, {'date': '2000-01', 'value': 168.8}, {'date': '2000-02', 'value': 169.8}, {'date': '2000-03', 'value': 171.2}, {'date': '2000-04', 'value': 171.3}, {'date': '2000-05', 'value': 171.5}, {'date': '2000-06', 'value': 172.4}, {'date': '2000-07', 'value': 172.8}, {'date': '2000-08', 'value': 172.8}, {'date': '2000-09', 'value': 173.7}, {'date': '2000-10', 'value': 174.0}, {'date': '2000-11', 'value': 174.1}, {'date': '2000-12', 'value': 174.0}, {'date': '2001-01', 'value': 175.1}, {'date': '2001-02', 'value': 175.8}, {'date': '2001-03', 'value': 176.2}, {'date': '2001-04', 'value': 176.9}, {'date': '2001-05', 'value': 177.7}, {'date': '2001-06', 'value': 178.0}, {'date': '2001-07', 'value': 177.5}, {'date': '2001-08', 'value': 177.5}, {'date': '2001-09', 'value': 178.3}, {'date': '2001-10', 'value': 177.7}, {'date': '2001-11', 'value': 177.4}, {'date': '2001-12', 'value': 176.7}, {'date': '2002-01', 'value': 177.1}, {'date': '2002-02', 'value': 177.8}, {'date': '2002-03', 'value': 178.8}, {'date': '2002-04', 'value': 179.8}, {'date': '2002-05', 'value': 179.8}, {'date': '2002-06', 'value': 179.9}, {'date': '2002-07', 'value': 180.1}, {'date': '2002-08', 'value': 180.7}, {'date': '2002-09', 'value': 181.0}, {'date': '2002-10', 'value': 181.3}, {'date': '2002-11', 'value': 181.3}, {'date': '2002-12', 'value': 180.9}, {'date': '2003-01', 'value': 181.7}, {'date': '2003-02', 'value': 183.1}, {'date': '2003-03', 'value': 184.2}, {'date': '2003-04', 'value': 183.8}, {'date': '2003-05', 'value': 183.5}, {'date': '2003-06', 'value': 183.7}, {'date': '2003-07', 'value': 183.9}, {'date': '2003-08', 'value': 184.6}, {'date': '2003-09', 'value': 185.2}, {'date': '2003-10', 'value': 185.0}, {'date': '2003-11', 'value': 184.5}, {'date': '2003-12', 'value': 184.3}, {'date': '2004-01', 'value': 185.2}, {'date': '2004-02', 'value': 186.2}, {'date': '2004-03', 'value': 187.4}, {'date': '2004-04', 'value': 188.0}, {'date': '2004-05', 'value': 189.1}, {'date': '2004-06', 'value': 189.7}, {'date': '2004-07', 'value': 189.4}, {'date': '2004-08', 'value': 189.5}, {'date': '2004-09', 'value': 189.9}, {'date': '2004-10', 'value': 190.9}, {'date': '2004-11', 'value': 191.0}, {'date': '2004-12', 'value': 190.3}, {'date': '2005-01', 'value': 190.7}, {'date': '2005-02', 'value': 191.8}, {'date': '2005-03', 'value': 193.3}, {'date': '2005-04', 'value': 194.6}, {'date': '2005-05', 'value': 194.4}, {'date': '2005-06', 'value': 194.5}, {'date': '2005-07', 'value': 195.4}, {'date': '2005-08', 'value': 196.4}, {'date': '2005-09', 'value': 198.8}, {'date': '2005-10', 'value': 199.2}, {'date': '2005-11', 'value': 197.6}, {'date': '2005-12', 'value': 196.8}, {'date': '2006-01', 'value': 198.3}, {'date': '2006-02', 'value': 198.7}, {'date': '2006-03', 'value': 199.8}, {'date': '2006-04', 'value': 201.5}, {'date': '2006-05', 'value': 202.5}, {'date': '2006-06', 'value': 202.9}, {'date': '2006-07', 'value': 203.5}, {'date': '2006-08', 'value': 203.9}, {'date': '2006-09', 'value': 202.9}, {'date': '2006-10', 'value': 201.8}, {'date': '2006-11', 'value': 201.5}, {'date': '2006-12', 'value': 201.8}, {'date': '2007-01', 'value': 202.416}, {'date': '2007-02', 'value': 203.499}, {'date': '2007-03', 'value': 205.352}, {'date': '2007-04', 'value': 206.686}, {'date': '2007-05', 'value': 207.949}, {'date': '2007-06', 'value': 208.352}, {'date': '2007-07', 'value': 208.299}, {'date': '2007-08', 'value': 207.917}, {'date': '2007-09', 'value': 208.49}, {'date': '2007-10', 'value': 208.936}, {'date': '2007-11', 'value': 210.177}, {'date': '2007-12', 'value': 210.036}, {'date': '2008-01', 'value': 211.08}, {'date': '2008-02', 'value': 211.693}, {'date': '2008-03', 'value': 213.528}, {'date': '2008-04', 'value': 214.823}, {'date': '2008-05', 'value': 216.632}, {'date': '2008-06', 'value': 218.815}, {'date': '2008-07', 'value': 219.964}, {'date': '2008-08', 'value': 219.086}, {'date': '2008-09', 'value': 218.783}, {'date': '2008-10', 'value': 216.573}, {'date': '2008-11', 'value': 212.425}, {'date': '2008-12', 'value': 210.228}, {'date': '2009-01', 'value': 211.143}, {'date': '2009-02', 'value': 212.193}, {'date': '2009-03', 'value': 212.709}, {'date': '2009-04', 'value': 213.24}, {'date': '2009-05', 'value': 213.856}, {'date': '2009-06', 'value': 215.693}, {'date': '2009-07', 'value': 215.351}, {'date': '2009-08', 'value': 215.834}, {'date': '2009-09', 'value': 215.969}, {'date': '2009-10', 'value': 216.177}, {'date': '2009-11', 'value': 216.33}, {'date': '2009-12', 'value': 215.949}, {'date': '2010-01', 'value': 216.687}, {'date': '2010-02', 'value': 216.741}, {'date': '2010-03', 'value': 217.631}, {'date': '2010-04', 'value': 218.009}, {'date': '2010-05', 'value': 218.178}, {'date': '2010-06', 'value': 217.965}, {'date': '2010-07', 'value': 218.011}, {'date': '2010-08', 'value': 218.312}, {'date': '2010-09', 'value': 218.439}, {'date': '2010-10', 'value': 218.711}, {'date': '2010-11', 'value': 218.803}, {'date': '2010-12', 'value': 219.179}, {'date': '2011-01', 'value': 220.223}, {'date': '2011-02', 'value': 221.309}, {'date': '2011-03', 'value': 223.467}, {'date': '2011-04', 'value': 224.906}, {'date': '2011-05', 'value': 225.964}, {'date': '2011-06', 'value': 225.722}, {'date': '2011-07', 'value': 225.922}, {'date': '2011-08', 'value': 226.545}, {'date': '2011-09', 'value': 226.889}, {'date': '2011-10', 'value': 226.421}, {'date': '2011-11', 'value': 226.23}, {'date': '2011-12', 'value': 225.672}, {'date': '2012-01', 'value': 226.665}, {'date': '2012-02', 'value': 227.663}, {'date': '2012-03', 'value': 229.392}, {'date': '2012-04', 'value': 230.085}, {'date': '2012-05', 'value': 229.815}, {'date': '2012-06', 'value': 229.478}, {'date': '2012-07', 'value': 229.104}, {'date': '2012-08', 'value': 230.379}, {'date': '2012-09', 'value': 231.407}, {'date': '2012-10', 'value': 231.317}, {'date': '2012-11', 'value': 230.221}, {'date': '2012-12', 'value': 229.601}, {'date': '2013-01', 'value': 230.28}, {'date': '2013-02', 'value': 232.166}, {'date': '2013-03', 'value': 232.773}, {'date': '2013-04', 'value': 232.531}, {'date': '2013-05', 'value': 232.945}, {'date': '2013-06', 'value': 233.504}, {'date': '2013-07', 'value': 233.596}, {'date': '2013-08', 'value': 233.877}, {'date': '2013-09', 'value': 234.149}, {'date': '2013-10', 'value': 233.546}, {'date': '2013-11', 'value': 233.069}, {'date': '2013-12', 'value': 233.049}, {'date': '2014-01', 'value': 233.916}, {'date': '2014-02', 'value': 234.781}, {'date': '2014-03', 'value': 236.293}, {'date': '2014-04', 'value': 237.072}, {'date': '2014-05', 'value': 237.9}, {'date': '2014-06', 'value': 238.343}, {'date': '2014-07', 'value': 238.25}, {'date': '2014-08', 'value': 237.852}, {'date': '2014-09', 'value': 238.031}, {'date': '2014-10', 'value': 237.433}, {'date': '2014-11', 'value': 236.151}, {'date': '2014-12', 'value': 234.812}, {'date': '2015-01', 'value': 233.707}, {'date': '2015-02', 'value': 234.722}, {'date': '2015-03', 'value': 236.119}, {'date': '2015-04', 'value': 236.599}, {'date': '2015-05', 'value': 237.805}, {'date': '2015-06', 'value': 238.638}, {'date': '2015-07', 'value': 238.654}, {'date': '2015-08', 'value': 238.316}, {'date': '2015-09', 'value': 237.945}, {'date': '2015-10', 'value': 237.838}, {'date': '2015-11', 'value': 237.336}, {'date': '2015-12', 'value': 236.525}, {'date': '2016-01', 'value': 236.916}, {'date': '2016-02', 'value': 237.111}, {'date': '2016-03', 'value': 238.132}, {'date': '2016-04', 'value': 239.261}, {'date': '2016-05', 'value': 240.229}, {'date': '2016-06', 'value': 241.018}, {'date': '2016-07', 'value': 240.628}, {'date': '2016-08', 'value': 240.849}, {'date': '2016-09', 'value': 241.428}, {'date': '2016-10', 'value': 241.729}, {'date': '2016-11', 'value': 241.353}, {'date': '2016-12', 'value': 241.432}, {'date': '2017-01', 'value': 242.839}, {'date': '2017-02', 'value': 243.603}, {'date': '2017-03', 'value': 243.801}, {'date': '2017-04', 'value': 244.524}, {'date': '2017-05', 'value': 244.733}, {'date': '2017-06', 'value': 244.955}, {'date': '2017-07', 'value': 244.786}, {'date': '2017-08', 'value': 245.519}, {'date': '2017-09', 'value': 246.819}, {'date': '2017-10', 'value': 246.663}, {'date': '2017-11', 'value': 246.669}, {'date': '2017-12', 'value': 246.524}, {'date': '2018-01', 'value': 247.867}, {'date': '2018-02', 'value': 248.991}, {'date': '2018-03', 'value': 249.554}, {'date': '2018-04', 'value': 250.546}, {'date': '2018-05', 'value': 251.588}, {'date': '2018-06', 'value': 251.989}, {'date': '2018-07', 'value': 252.006}, {'date': '2018-08', 'value': 252.146}, {'date': '2018-09', 'value': 252.439}, {'date': '2018-10', 'value': 252.885}, {'date': '2018-11', 'value': 252.038}, {'date': '2018-12', 'value': 251.233}, {'date': '2019-01', 'value': 251.712}, {'date': '2019-02', 'value': 252.776}, {'date': '2019-03', 'value': 254.202}, {'date': '2019-04', 'value': 255.548}, {'date': '2019-05', 'value': 256.092}, {'date': '2019-06', 'value': 256.143}, {'date': '2019-07', 'value': 256.571}, {'date': '2019-08', 'value': 256.558}, {'date': '2019-09', 'value': 256.759}, {'date': '2019-10', 'value': 257.346}, {'date': '2019-11', 'value': 257.208}, {'date': '2019-12', 'value': 256.974}, {'date': '2020-01', 'value': 257.971}, {'date': '2020-02', 'value': 258.678}, {'date': '2020-03', 'value': 258.115}, {'date': '2020-04', 'value': 256.389}, {'date': '2020-05', 'value': 256.394}, {'date': '2020-06', 'value': 257.797}, {'date': '2020-07', 'value': 259.101}, {'date': '2020-08', 'value': 259.918}, {'date': '2020-09', 'value': 260.28}, {'date': '2020-10', 'value': 260.388}, {'date': '2020-11', 'value': 260.229}, {'date': '2020-12', 'value': 260.474}, {'date': '2021-01', 'value': 261.582}, {'date': '2021-02', 'value': 263.014}, {'date': '2021-03', 'value': 264.877}, {'date': '2021-04', 'value': 267.054}, {'date': '2021-05', 'value': 269.195}, {'date': '2021-06', 'value': 271.696}, {'date': '2021-07', 'value': 273.003}, {'date': '2021-08', 'value': 273.567}, {'date': '2021-09', 'value': 274.31}, {'date': '2021-10', 'value': 276.589}, {'date': '2021-11', 'value': 277.948}, {'date': '2021-12', 'value': 278.802}, {'date': '2022-01', 'value': 281.148}, {'date': '2022-02', 'value': 283.716}, {'date': '2022-03', 'value': 287.504}, {'date': '2022-04', 'value': 289.109}, {'date': '2022-05', 'value': 292.296}, {'date': '2022-06', 'value': 296.311}, {'date': '2022-07', 'value': 296.276}, {'date': '2022-08', 'value': 296.171}, {'date': '2022-09', 'value': 296.808}, {'date': '2022-10', 'value': 298.012}, {'date': '2022-11', 'value': 297.711}, {'date': '2022-12', 'value': 296.797}, {'date': '2023-01', 'value': 299.17}, {'date': '2023-02', 'value': 300.84}, {'date': '2023-03', 'value': 301.836}, {'date': '2023-04', 'value': 303.363}, {'date': '2023-05', 'value': 304.127}, {'date': '2023-06', 'value': 305.109}, {'date': '2023-07', 'value': 305.691}, {'date': '2023-08', 'value': 307.026}, {'date': '2023-09', 'value': 307.789}, {'date': '2023-10', 'value': 307.671}, {'date': '2023-11', 'value': 307.051}, {'date': '2023-12', 'value': 306.746}, {'date': '2024-01', 'value': 308.417}, {'date': '2024-02', 'value': 310.326}, {'date': '2024-03', 'value': 312.332}, {'date': '2024-04', 'value': 313.548}, {'date': '2024-05', 'value': 314.069}]

@st.cache_data
def get_bls_unemployment_data_statically():

    print('Not cached - BLS data')
    # See https://data.bls.gov/timeseries/LNS14000000

    return [{'date': '1948-01', 'value': 3.4}, {'date': '1948-02', 'value': 3.8}, {'date': '1948-03', 'value': 4.0}, {'date': '1948-04', 'value': 3.9}, {'date': '1948-05', 'value': 3.5}, {'date': '1948-06', 'value': 3.6}, {'date': '1948-07', 'value': 3.6}, {'date': '1948-08', 'value': 3.9}, {'date': '1948-09', 'value': 3.8}, {'date': '1948-10', 'value': 3.7}, {'date': '1948-11', 'value': 3.8}, {'date': '1948-12', 'value': 4.0}, {'date': '1949-01', 'value': 4.3}, {'date': '1949-02', 'value': 4.7}, {'date': '1949-03', 'value': 5.0}, {'date': '1949-04', 'value': 5.3}, {'date': '1949-05', 'value': 6.1}, {'date': '1949-06', 'value': 6.2}, {'date': '1949-07', 'value': 6.7}, {'date': '1949-08', 'value': 6.8}, {'date': '1949-09', 'value': 6.6}, {'date': '1949-10', 'value': 7.9}, {'date': '1949-11', 'value': 6.4}, {'date': '1949-12', 'value': 6.6}, {'date': '1950-01', 'value': 6.5}, {'date': '1950-02', 'value': 6.4}, {'date': '1950-03', 'value': 6.3}, {'date': '1950-04', 'value': 5.8}, {'date': '1950-05', 'value': 5.5}, {'date': '1950-06', 'value': 5.4}, {'date': '1950-07', 'value': 5.0}, {'date': '1950-08', 'value': 4.5}, {'date': '1950-09', 'value': 4.4}, {'date': '1950-10', 'value': 4.2}, {'date': '1950-11', 'value': 4.2}, {'date': '1950-12', 'value': 4.3}, {'date': '1951-01', 'value': 3.7}, {'date': '1951-02', 'value': 3.4}, {'date': '1951-03', 'value': 3.4}, {'date': '1951-04', 'value': 3.1}, {'date': '1951-05', 'value': 3.0}, {'date': '1951-06', 'value': 3.2}, {'date': '1951-07', 'value': 3.1}, {'date': '1951-08', 'value': 3.1}, {'date': '1951-09', 'value': 3.3}, {'date': '1951-10', 'value': 3.5}, {'date': '1951-11', 'value': 3.5}, {'date': '1951-12', 'value': 3.1}, {'date': '1952-01', 'value': 3.2}, {'date': '1952-02', 'value': 3.1}, {'date': '1952-03', 'value': 2.9}, {'date': '1952-04', 'value': 2.9}, {'date': '1952-05', 'value': 3.0}, {'date': '1952-06', 'value': 3.0}, {'date': '1952-07', 'value': 3.2}, {'date': '1952-08', 'value': 3.4}, {'date': '1952-09', 'value': 3.1}, {'date': '1952-10', 'value': 3.0}, {'date': '1952-11', 'value': 2.8}, {'date': '1952-12', 'value': 2.7}, {'date': '1953-01', 'value': 2.9}, {'date': '1953-02', 'value': 2.6}, {'date': '1953-03', 'value': 2.6}, {'date': '1953-04', 'value': 2.7}, {'date': '1953-05', 'value': 2.5}, {'date': '1953-06', 'value': 2.5}, {'date': '1953-07', 'value': 2.6}, {'date': '1953-08', 'value': 2.7}, {'date': '1953-09', 'value': 2.9}, {'date': '1953-10', 'value': 3.1}, {'date': '1953-11', 'value': 3.5}, {'date': '1953-12', 'value': 4.5}, {'date': '1954-01', 'value': 4.9}, {'date': '1954-02', 'value': 5.2}, {'date': '1954-03', 'value': 5.7}, {'date': '1954-04', 'value': 5.9}, {'date': '1954-05', 'value': 5.9}, {'date': '1954-06', 'value': 5.6}, {'date': '1954-07', 'value': 5.8}, {'date': '1954-08', 'value': 6.0}, {'date': '1954-09', 'value': 6.1}, {'date': '1954-10', 'value': 5.7}, {'date': '1954-11', 'value': 5.3}, {'date': '1954-12', 'value': 5.0}, {'date': '1955-01', 'value': 4.9}, {'date': '1955-02', 'value': 4.7}, {'date': '1955-03', 'value': 4.6}, {'date': '1955-04', 'value': 4.7}, {'date': '1955-05', 'value': 4.3}, {'date': '1955-06', 'value': 4.2}, {'date': '1955-07', 'value': 4.0}, {'date': '1955-08', 'value': 4.2}, {'date': '1955-09', 'value': 4.1}, {'date': '1955-10', 'value': 4.3}, {'date': '1955-11', 'value': 4.2}, {'date': '1955-12', 'value': 4.2}, {'date': '1956-01', 'value': 4.0}, {'date': '1956-02', 'value': 3.9}, {'date': '1956-03', 'value': 4.2}, {'date': '1956-04', 'value': 4.0}, {'date': '1956-05', 'value': 4.3}, {'date': '1956-06', 'value': 4.3}, {'date': '1956-07', 'value': 4.4}, {'date': '1956-08', 'value': 4.1}, {'date': '1956-09', 'value': 3.9}, {'date': '1956-10', 'value': 3.9}, {'date': '1956-11', 'value': 4.3}, {'date': '1956-12', 'value': 4.2}, {'date': '1957-01', 'value': 4.2}, {'date': '1957-02', 'value': 3.9}, {'date': '1957-03', 'value': 3.7}, {'date': '1957-04', 'value': 3.9}, {'date': '1957-05', 'value': 4.1}, {'date': '1957-06', 'value': 4.3}, {'date': '1957-07', 'value': 4.2}, {'date': '1957-08', 'value': 4.1}, {'date': '1957-09', 'value': 4.4}, {'date': '1957-10', 'value': 4.5}, {'date': '1957-11', 'value': 5.1}, {'date': '1957-12', 'value': 5.2}, {'date': '1958-01', 'value': 5.8}, {'date': '1958-02', 'value': 6.4}, {'date': '1958-03', 'value': 6.7}, {'date': '1958-04', 'value': 7.4}, {'date': '1958-05', 'value': 7.4}, {'date': '1958-06', 'value': 7.3}, {'date': '1958-07', 'value': 7.5}, {'date': '1958-08', 'value': 7.4}, {'date': '1958-09', 'value': 7.1}, {'date': '1958-10', 'value': 6.7}, {'date': '1958-11', 'value': 6.2}, {'date': '1958-12', 'value': 6.2}, {'date': '1959-01', 'value': 6.0}, {'date': '1959-02', 'value': 5.9}, {'date': '1959-03', 'value': 5.6}, {'date': '1959-04', 'value': 5.2}, {'date': '1959-05', 'value': 5.1}, {'date': '1959-06', 'value': 5.0}, {'date': '1959-07', 'value': 5.1}, {'date': '1959-08', 'value': 5.2}, {'date': '1959-09', 'value': 5.5}, {'date': '1959-10', 'value': 5.7}, {'date': '1959-11', 'value': 5.8}, {'date': '1959-12', 'value': 5.3}, {'date': '1960-01', 'value': 5.2}, {'date': '1960-02', 'value': 4.8}, {'date': '1960-03', 'value': 5.4}, {'date': '1960-04', 'value': 5.2}, {'date': '1960-05', 'value': 5.1}, {'date': '1960-06', 'value': 5.4}, {'date': '1960-07', 'value': 5.5}, {'date': '1960-08', 'value': 5.6}, {'date': '1960-09', 'value': 5.5}, {'date': '1960-10', 'value': 6.1}, {'date': '1960-11', 'value': 6.1}, {'date': '1960-12', 'value': 6.6}, {'date': '1961-01', 'value': 6.6}, {'date': '1961-02', 'value': 6.9}, {'date': '1961-03', 'value': 6.9}, {'date': '1961-04', 'value': 7.0}, {'date': '1961-05', 'value': 7.1}, {'date': '1961-06', 'value': 6.9}, {'date': '1961-07', 'value': 7.0}, {'date': '1961-08', 'value': 6.6}, {'date': '1961-09', 'value': 6.7}, {'date': '1961-10', 'value': 6.5}, {'date': '1961-11', 'value': 6.1}, {'date': '1961-12', 'value': 6.0}, {'date': '1962-01', 'value': 5.8}, {'date': '1962-02', 'value': 5.5}, {'date': '1962-03', 'value': 5.6}, {'date': '1962-04', 'value': 5.6}, {'date': '1962-05', 'value': 5.5}, {'date': '1962-06', 'value': 5.5}, {'date': '1962-07', 'value': 5.4}, {'date': '1962-08', 'value': 5.7}, {'date': '1962-09', 'value': 5.6}, {'date': '1962-10', 'value': 5.4}, {'date': '1962-11', 'value': 5.7}, {'date': '1962-12', 'value': 5.5}, {'date': '1963-01', 'value': 5.7}, {'date': '1963-02', 'value': 5.9}, {'date': '1963-03', 'value': 5.7}, {'date': '1963-04', 'value': 5.7}, {'date': '1963-05', 'value': 5.9}, {'date': '1963-06', 'value': 5.6}, {'date': '1963-07', 'value': 5.6}, {'date': '1963-08', 'value': 5.4}, {'date': '1963-09', 'value': 5.5}, {'date': '1963-10', 'value': 5.5}, {'date': '1963-11', 'value': 5.7}, {'date': '1963-12', 'value': 5.5}, {'date': '1964-01', 'value': 5.6}, {'date': '1964-02', 'value': 5.4}, {'date': '1964-03', 'value': 5.4}, {'date': '1964-04', 'value': 5.3}, {'date': '1964-05', 'value': 5.1}, {'date': '1964-06', 'value': 5.2}, {'date': '1964-07', 'value': 4.9}, {'date': '1964-08', 'value': 5.0}, {'date': '1964-09', 'value': 5.1}, {'date': '1964-10', 'value': 5.1}, {'date': '1964-11', 'value': 4.8}, {'date': '1964-12', 'value': 5.0}, {'date': '1965-01', 'value': 4.9}, {'date': '1965-02', 'value': 5.1}, {'date': '1965-03', 'value': 4.7}, {'date': '1965-04', 'value': 4.8}, {'date': '1965-05', 'value': 4.6}, {'date': '1965-06', 'value': 4.6}, {'date': '1965-07', 'value': 4.4}, {'date': '1965-08', 'value': 4.4}, {'date': '1965-09', 'value': 4.3}, {'date': '1965-10', 'value': 4.2}, {'date': '1965-11', 'value': 4.1}, {'date': '1965-12', 'value': 4.0}, {'date': '1966-01', 'value': 4.0}, {'date': '1966-02', 'value': 3.8}, {'date': '1966-03', 'value': 3.8}, {'date': '1966-04', 'value': 3.8}, {'date': '1966-05', 'value': 3.9}, {'date': '1966-06', 'value': 3.8}, {'date': '1966-07', 'value': 3.8}, {'date': '1966-08', 'value': 3.8}, {'date': '1966-09', 'value': 3.7}, {'date': '1966-10', 'value': 3.7}, {'date': '1966-11', 'value': 3.6}, {'date': '1966-12', 'value': 3.8}, {'date': '1967-01', 'value': 3.9}, {'date': '1967-02', 'value': 3.8}, {'date': '1967-03', 'value': 3.8}, {'date': '1967-04', 'value': 3.8}, {'date': '1967-05', 'value': 3.8}, {'date': '1967-06', 'value': 3.9}, {'date': '1967-07', 'value': 3.8}, {'date': '1967-08', 'value': 3.8}, {'date': '1967-09', 'value': 3.8}, {'date': '1967-10', 'value': 4.0}, {'date': '1967-11', 'value': 3.9}, {'date': '1967-12', 'value': 3.8}, {'date': '1968-01', 'value': 3.7}, {'date': '1968-02', 'value': 3.8}, {'date': '1968-03', 'value': 3.7}, {'date': '1968-04', 'value': 3.5}, {'date': '1968-05', 'value': 3.5}, {'date': '1968-06', 'value': 3.7}, {'date': '1968-07', 'value': 3.7}, {'date': '1968-08', 'value': 3.5}, {'date': '1968-09', 'value': 3.4}, {'date': '1968-10', 'value': 3.4}, {'date': '1968-11', 'value': 3.4}, {'date': '1968-12', 'value': 3.4}, {'date': '1969-01', 'value': 3.4}, {'date': '1969-02', 'value': 3.4}, {'date': '1969-03', 'value': 3.4}, {'date': '1969-04', 'value': 3.4}, {'date': '1969-05', 'value': 3.4}, {'date': '1969-06', 'value': 3.5}, {'date': '1969-07', 'value': 3.5}, {'date': '1969-08', 'value': 3.5}, {'date': '1969-09', 'value': 3.7}, {'date': '1969-10', 'value': 3.7}, {'date': '1969-11', 'value': 3.5}, {'date': '1969-12', 'value': 3.5}, {'date': '1970-01', 'value': 3.9}, {'date': '1970-02', 'value': 4.2}, {'date': '1970-03', 'value': 4.4}, {'date': '1970-04', 'value': 4.6}, {'date': '1970-05', 'value': 4.8}, {'date': '1970-06', 'value': 4.9}, {'date': '1970-07', 'value': 5.0}, {'date': '1970-08', 'value': 5.1}, {'date': '1970-09', 'value': 5.4}, {'date': '1970-10', 'value': 5.5}, {'date': '1970-11', 'value': 5.9}, {'date': '1970-12', 'value': 6.1}, {'date': '1971-01', 'value': 5.9}, {'date': '1971-02', 'value': 5.9}, {'date': '1971-03', 'value': 6.0}, {'date': '1971-04', 'value': 5.9}, {'date': '1971-05', 'value': 5.9}, {'date': '1971-06', 'value': 5.9}, {'date': '1971-07', 'value': 6.0}, {'date': '1971-08', 'value': 6.1}, {'date': '1971-09', 'value': 6.0}, {'date': '1971-10', 'value': 5.8}, {'date': '1971-11', 'value': 6.0}, {'date': '1971-12', 'value': 6.0}, {'date': '1972-01', 'value': 5.8}, {'date': '1972-02', 'value': 5.7}, {'date': '1972-03', 'value': 5.8}, {'date': '1972-04', 'value': 5.7}, {'date': '1972-05', 'value': 5.7}, {'date': '1972-06', 'value': 5.7}, {'date': '1972-07', 'value': 5.6}, {'date': '1972-08', 'value': 5.6}, {'date': '1972-09', 'value': 5.5}, {'date': '1972-10', 'value': 5.6}, {'date': '1972-11', 'value': 5.3}, {'date': '1972-12', 'value': 5.2}, {'date': '1973-01', 'value': 4.9}, {'date': '1973-02', 'value': 5.0}, {'date': '1973-03', 'value': 4.9}, {'date': '1973-04', 'value': 5.0}, {'date': '1973-05', 'value': 4.9}, {'date': '1973-06', 'value': 4.9}, {'date': '1973-07', 'value': 4.8}, {'date': '1973-08', 'value': 4.8}, {'date': '1973-09', 'value': 4.8}, {'date': '1973-10', 'value': 4.6}, {'date': '1973-11', 'value': 4.8}, {'date': '1973-12', 'value': 4.9}, {'date': '1974-01', 'value': 5.1}, {'date': '1974-02', 'value': 5.2}, {'date': '1974-03', 'value': 5.1}, {'date': '1974-04', 'value': 5.1}, {'date': '1974-05', 'value': 5.1}, {'date': '1974-06', 'value': 5.4}, {'date': '1974-07', 'value': 5.5}, {'date': '1974-08', 'value': 5.5}, {'date': '1974-09', 'value': 5.9}, {'date': '1974-10', 'value': 6.0}, {'date': '1974-11', 'value': 6.6}, {'date': '1974-12', 'value': 7.2}, {'date': '1975-01', 'value': 8.1}, {'date': '1975-02', 'value': 8.1}, {'date': '1975-03', 'value': 8.6}, {'date': '1975-04', 'value': 8.8}, {'date': '1975-05', 'value': 9.0}, {'date': '1975-06', 'value': 8.8}, {'date': '1975-07', 'value': 8.6}, {'date': '1975-08', 'value': 8.4}, {'date': '1975-09', 'value': 8.4}, {'date': '1975-10', 'value': 8.4}, {'date': '1975-11', 'value': 8.3}, {'date': '1975-12', 'value': 8.2}, {'date': '1976-01', 'value': 7.9}, {'date': '1976-02', 'value': 7.7}, {'date': '1976-03', 'value': 7.6}, {'date': '1976-04', 'value': 7.7}, {'date': '1976-05', 'value': 7.4}, {'date': '1976-06', 'value': 7.6}, {'date': '1976-07', 'value': 7.8}, {'date': '1976-08', 'value': 7.8}, {'date': '1976-09', 'value': 7.6}, {'date': '1976-10', 'value': 7.7}, {'date': '1976-11', 'value': 7.8}, {'date': '1976-12', 'value': 7.8}, {'date': '1977-01', 'value': 7.5}, {'date': '1977-02', 'value': 7.6}, {'date': '1977-03', 'value': 7.4}, {'date': '1977-04', 'value': 7.2}, {'date': '1977-05', 'value': 7.0}, {'date': '1977-06', 'value': 7.2}, {'date': '1977-07', 'value': 6.9}, {'date': '1977-08', 'value': 7.0}, {'date': '1977-09', 'value': 6.8}, {'date': '1977-10', 'value': 6.8}, {'date': '1977-11', 'value': 6.8}, {'date': '1977-12', 'value': 6.4}, {'date': '1978-01', 'value': 6.4}, {'date': '1978-02', 'value': 6.3}, {'date': '1978-03', 'value': 6.3}, {'date': '1978-04', 'value': 6.1}, {'date': '1978-05', 'value': 6.0}, {'date': '1978-06', 'value': 5.9}, {'date': '1978-07', 'value': 6.2}, {'date': '1978-08', 'value': 5.9}, {'date': '1978-09', 'value': 6.0}, {'date': '1978-10', 'value': 5.8}, {'date': '1978-11', 'value': 5.9}, {'date': '1978-12', 'value': 6.0}, {'date': '1979-01', 'value': 5.9}, {'date': '1979-02', 'value': 5.9}, {'date': '1979-03', 'value': 5.8}, {'date': '1979-04', 'value': 5.8}, {'date': '1979-05', 'value': 5.6}, {'date': '1979-06', 'value': 5.7}, {'date': '1979-07', 'value': 5.7}, {'date': '1979-08', 'value': 6.0}, {'date': '1979-09', 'value': 5.9}, {'date': '1979-10', 'value': 6.0}, {'date': '1979-11', 'value': 5.9}, {'date': '1979-12', 'value': 6.0}, {'date': '1980-01', 'value': 6.3}, {'date': '1980-02', 'value': 6.3}, {'date': '1980-03', 'value': 6.3}, {'date': '1980-04', 'value': 6.9}, {'date': '1980-05', 'value': 7.5}, {'date': '1980-06', 'value': 7.6}, {'date': '1980-07', 'value': 7.8}, {'date': '1980-08', 'value': 7.7}, {'date': '1980-09', 'value': 7.5}, {'date': '1980-10', 'value': 7.5}, {'date': '1980-11', 'value': 7.5}, {'date': '1980-12', 'value': 7.2}, {'date': '1981-01', 'value': 7.5}, {'date': '1981-02', 'value': 7.4}, {'date': '1981-03', 'value': 7.4}, {'date': '1981-04', 'value': 7.2}, {'date': '1981-05', 'value': 7.5}, {'date': '1981-06', 'value': 7.5}, {'date': '1981-07', 'value': 7.2}, {'date': '1981-08', 'value': 7.4}, {'date': '1981-09', 'value': 7.6}, {'date': '1981-10', 'value': 7.9}, {'date': '1981-11', 'value': 8.3}, {'date': '1981-12', 'value': 8.5}, {'date': '1982-01', 'value': 8.6}, {'date': '1982-02', 'value': 8.9}, {'date': '1982-03', 'value': 9.0}, {'date': '1982-04', 'value': 9.3}, {'date': '1982-05', 'value': 9.4}, {'date': '1982-06', 'value': 9.6}, {'date': '1982-07', 'value': 9.8}, {'date': '1982-08', 'value': 9.8}, {'date': '1982-09', 'value': 10.1}, {'date': '1982-10', 'value': 10.4}, {'date': '1982-11', 'value': 10.8}, {'date': '1982-12', 'value': 10.8}, {'date': '1983-01', 'value': 10.4}, {'date': '1983-02', 'value': 10.4}, {'date': '1983-03', 'value': 10.3}, {'date': '1983-04', 'value': 10.2}, {'date': '1983-05', 'value': 10.1}, {'date': '1983-06', 'value': 10.1}, {'date': '1983-07', 'value': 9.4}, {'date': '1983-08', 'value': 9.5}, {'date': '1983-09', 'value': 9.2}, {'date': '1983-10', 'value': 8.8}, {'date': '1983-11', 'value': 8.5}, {'date': '1983-12', 'value': 8.3}, {'date': '1984-01', 'value': 8.0}, {'date': '1984-02', 'value': 7.8}, {'date': '1984-03', 'value': 7.8}, {'date': '1984-04', 'value': 7.7}, {'date': '1984-05', 'value': 7.4}, {'date': '1984-06', 'value': 7.2}, {'date': '1984-07', 'value': 7.5}, {'date': '1984-08', 'value': 7.5}, {'date': '1984-09', 'value': 7.3}, {'date': '1984-10', 'value': 7.4}, {'date': '1984-11', 'value': 7.2}, {'date': '1984-12', 'value': 7.3}, {'date': '1985-01', 'value': 7.3}, {'date': '1985-02', 'value': 7.2}, {'date': '1985-03', 'value': 7.2}, {'date': '1985-04', 'value': 7.3}, {'date': '1985-05', 'value': 7.2}, {'date': '1985-06', 'value': 7.4}, {'date': '1985-07', 'value': 7.4}, {'date': '1985-08', 'value': 7.1}, {'date': '1985-09', 'value': 7.1}, {'date': '1985-10', 'value': 7.1}, {'date': '1985-11', 'value': 7.0}, {'date': '1985-12', 'value': 7.0}, {'date': '1986-01', 'value': 6.7}, {'date': '1986-02', 'value': 7.2}, {'date': '1986-03', 'value': 7.2}, {'date': '1986-04', 'value': 7.1}, {'date': '1986-05', 'value': 7.2}, {'date': '1986-06', 'value': 7.2}, {'date': '1986-07', 'value': 7.0}, {'date': '1986-08', 'value': 6.9}, {'date': '1986-09', 'value': 7.0}, {'date': '1986-10', 'value': 7.0}, {'date': '1986-11', 'value': 6.9}, {'date': '1986-12', 'value': 6.6}, {'date': '1987-01', 'value': 6.6}, {'date': '1987-02', 'value': 6.6}, {'date': '1987-03', 'value': 6.6}, {'date': '1987-04', 'value': 6.3}, {'date': '1987-05', 'value': 6.3}, {'date': '1987-06', 'value': 6.2}, {'date': '1987-07', 'value': 6.1}, {'date': '1987-08', 'value': 6.0}, {'date': '1987-09', 'value': 5.9}, {'date': '1987-10', 'value': 6.0}, {'date': '1987-11', 'value': 5.8}, {'date': '1987-12', 'value': 5.7}, {'date': '1988-01', 'value': 5.7}, {'date': '1988-02', 'value': 5.7}, {'date': '1988-03', 'value': 5.7}, {'date': '1988-04', 'value': 5.4}, {'date': '1988-05', 'value': 5.6}, {'date': '1988-06', 'value': 5.4}, {'date': '1988-07', 'value': 5.4}, {'date': '1988-08', 'value': 5.6}, {'date': '1988-09', 'value': 5.4}, {'date': '1988-10', 'value': 5.4}, {'date': '1988-11', 'value': 5.3}, {'date': '1988-12', 'value': 5.3}, {'date': '1989-01', 'value': 5.4}, {'date': '1989-02', 'value': 5.2}, {'date': '1989-03', 'value': 5.0}, {'date': '1989-04', 'value': 5.2}, {'date': '1989-05', 'value': 5.2}, {'date': '1989-06', 'value': 5.3}, {'date': '1989-07', 'value': 5.2}, {'date': '1989-08', 'value': 5.2}, {'date': '1989-09', 'value': 5.3}, {'date': '1989-10', 'value': 5.3}, {'date': '1989-11', 'value': 5.4}, {'date': '1989-12', 'value': 5.4}, {'date': '1990-01', 'value': 5.4}, {'date': '1990-02', 'value': 5.3}, {'date': '1990-03', 'value': 5.2}, {'date': '1990-04', 'value': 5.4}, {'date': '1990-05', 'value': 5.4}, {'date': '1990-06', 'value': 5.2}, {'date': '1990-07', 'value': 5.5}, {'date': '1990-08', 'value': 5.7}, {'date': '1990-09', 'value': 5.9}, {'date': '1990-10', 'value': 5.9}, {'date': '1990-11', 'value': 6.2}, {'date': '1990-12', 'value': 6.3}, {'date': '1991-01', 'value': 6.4}, {'date': '1991-02', 'value': 6.6}, {'date': '1991-03', 'value': 6.8}, {'date': '1991-04', 'value': 6.7}, {'date': '1991-05', 'value': 6.9}, {'date': '1991-06', 'value': 6.9}, {'date': '1991-07', 'value': 6.8}, {'date': '1991-08', 'value': 6.9}, {'date': '1991-09', 'value': 6.9}, {'date': '1991-10', 'value': 7.0}, {'date': '1991-11', 'value': 7.0}, {'date': '1991-12', 'value': 7.3}, {'date': '1992-01', 'value': 7.3}, {'date': '1992-02', 'value': 7.4}, {'date': '1992-03', 'value': 7.4}, {'date': '1992-04', 'value': 7.4}, {'date': '1992-05', 'value': 7.6}, {'date': '1992-06', 'value': 7.8}, {'date': '1992-07', 'value': 7.7}, {'date': '1992-08', 'value': 7.6}, {'date': '1992-09', 'value': 7.6}, {'date': '1992-10', 'value': 7.3}, {'date': '1992-11', 'value': 7.4}, {'date': '1992-12', 'value': 7.4}, {'date': '1993-01', 'value': 7.3}, {'date': '1993-02', 'value': 7.1}, {'date': '1993-03', 'value': 7.0}, {'date': '1993-04', 'value': 7.1}, {'date': '1993-05', 'value': 7.1}, {'date': '1993-06', 'value': 7.0}, {'date': '1993-07', 'value': 6.9}, {'date': '1993-08', 'value': 6.8}, {'date': '1993-09', 'value': 6.7}, {'date': '1993-10', 'value': 6.8}, {'date': '1993-11', 'value': 6.6}, {'date': '1993-12', 'value': 6.5}, {'date': '1994-01', 'value': 6.6}, {'date': '1994-02', 'value': 6.6}, {'date': '1994-03', 'value': 6.5}, {'date': '1994-04', 'value': 6.4}, {'date': '1994-05', 'value': 6.1}, {'date': '1994-06', 'value': 6.1}, {'date': '1994-07', 'value': 6.1}, {'date': '1994-08', 'value': 6.0}, {'date': '1994-09', 'value': 5.9}, {'date': '1994-10', 'value': 5.8}, {'date': '1994-11', 'value': 5.6}, {'date': '1994-12', 'value': 5.5}, {'date': '1995-01', 'value': 5.6}, {'date': '1995-02', 'value': 5.4}, {'date': '1995-03', 'value': 5.4}, {'date': '1995-04', 'value': 5.8}, {'date': '1995-05', 'value': 5.6}, {'date': '1995-06', 'value': 5.6}, {'date': '1995-07', 'value': 5.7}, {'date': '1995-08', 'value': 5.7}, {'date': '1995-09', 'value': 5.6}, {'date': '1995-10', 'value': 5.5}, {'date': '1995-11', 'value': 5.6}, {'date': '1995-12', 'value': 5.6}, {'date': '1996-01', 'value': 5.6}, {'date': '1996-02', 'value': 5.5}, {'date': '1996-03', 'value': 5.5}, {'date': '1996-04', 'value': 5.6}, {'date': '1996-05', 'value': 5.6}, {'date': '1996-06', 'value': 5.3}, {'date': '1996-07', 'value': 5.5}, {'date': '1996-08', 'value': 5.1}, {'date': '1996-09', 'value': 5.2}, {'date': '1996-10', 'value': 5.2}, {'date': '1996-11', 'value': 5.4}, {'date': '1996-12', 'value': 5.4}, {'date': '1997-01', 'value': 5.3}, {'date': '1997-02', 'value': 5.2}, {'date': '1997-03', 'value': 5.2}, {'date': '1997-04', 'value': 5.1}, {'date': '1997-05', 'value': 4.9}, {'date': '1997-06', 'value': 5.0}, {'date': '1997-07', 'value': 4.9}, {'date': '1997-08', 'value': 4.8}, {'date': '1997-09', 'value': 4.9}, {'date': '1997-10', 'value': 4.7}, {'date': '1997-11', 'value': 4.6}, {'date': '1997-12', 'value': 4.7}, {'date': '1998-01', 'value': 4.6}, {'date': '1998-02', 'value': 4.6}, {'date': '1998-03', 'value': 4.7}, {'date': '1998-04', 'value': 4.3}, {'date': '1998-05', 'value': 4.4}, {'date': '1998-06', 'value': 4.5}, {'date': '1998-07', 'value': 4.5}, {'date': '1998-08', 'value': 4.5}, {'date': '1998-09', 'value': 4.6}, {'date': '1998-10', 'value': 4.5}, {'date': '1998-11', 'value': 4.4}, {'date': '1998-12', 'value': 4.4}, {'date': '1999-01', 'value': 4.3}, {'date': '1999-02', 'value': 4.4}, {'date': '1999-03', 'value': 4.2}, {'date': '1999-04', 'value': 4.3}, {'date': '1999-05', 'value': 4.2}, {'date': '1999-06', 'value': 4.3}, {'date': '1999-07', 'value': 4.3}, {'date': '1999-08', 'value': 4.2}, {'date': '1999-09', 'value': 4.2}, {'date': '1999-10', 'value': 4.1}, {'date': '1999-11', 'value': 4.1}, {'date': '1999-12', 'value': 4.0}, {'date': '2000-01', 'value': 4.0}, {'date': '2000-02', 'value': 4.1}, {'date': '2000-03', 'value': 4.0}, {'date': '2000-04', 'value': 3.8}, {'date': '2000-05', 'value': 4.0}, {'date': '2000-06', 'value': 4.0}, {'date': '2000-07', 'value': 4.0}, {'date': '2000-08', 'value': 4.1}, {'date': '2000-09', 'value': 3.9}, {'date': '2000-10', 'value': 3.9}, {'date': '2000-11', 'value': 3.9}, {'date': '2000-12', 'value': 3.9}, {'date': '2001-01', 'value': 4.2}, {'date': '2001-02', 'value': 4.2}, {'date': '2001-03', 'value': 4.3}, {'date': '2001-04', 'value': 4.4}, {'date': '2001-05', 'value': 4.3}, {'date': '2001-06', 'value': 4.5}, {'date': '2001-07', 'value': 4.6}, {'date': '2001-08', 'value': 4.9}, {'date': '2001-09', 'value': 5.0}, {'date': '2001-10', 'value': 5.3}, {'date': '2001-11', 'value': 5.5}, {'date': '2001-12', 'value': 5.7}, {'date': '2002-01', 'value': 5.7}, {'date': '2002-02', 'value': 5.7}, {'date': '2002-03', 'value': 5.7}, {'date': '2002-04', 'value': 5.9}, {'date': '2002-05', 'value': 5.8}, {'date': '2002-06', 'value': 5.8}, {'date': '2002-07', 'value': 5.8}, {'date': '2002-08', 'value': 5.7}, {'date': '2002-09', 'value': 5.7}, {'date': '2002-10', 'value': 5.7}, {'date': '2002-11', 'value': 5.9}, {'date': '2002-12', 'value': 6.0}, {'date': '2003-01', 'value': 5.8}, {'date': '2003-02', 'value': 5.9}, {'date': '2003-03', 'value': 5.9}, {'date': '2003-04', 'value': 6.0}, {'date': '2003-05', 'value': 6.1}, {'date': '2003-06', 'value': 6.3}, {'date': '2003-07', 'value': 6.2}, {'date': '2003-08', 'value': 6.1}, {'date': '2003-09', 'value': 6.1}, {'date': '2003-10', 'value': 6.0}, {'date': '2003-11', 'value': 5.8}, {'date': '2003-12', 'value': 5.7}, {'date': '2004-01', 'value': 5.7}, {'date': '2004-02', 'value': 5.6}, {'date': '2004-03', 'value': 5.8}, {'date': '2004-04', 'value': 5.6}, {'date': '2004-05', 'value': 5.6}, {'date': '2004-06', 'value': 5.6}, {'date': '2004-07', 'value': 5.5}, {'date': '2004-08', 'value': 5.4}, {'date': '2004-09', 'value': 5.4}, {'date': '2004-10', 'value': 5.5}, {'date': '2004-11', 'value': 5.4}, {'date': '2004-12', 'value': 5.4}, {'date': '2005-01', 'value': 5.3}, {'date': '2005-02', 'value': 5.4}, {'date': '2005-03', 'value': 5.2}, {'date': '2005-04', 'value': 5.2}, {'date': '2005-05', 'value': 5.1}, {'date': '2005-06', 'value': 5.0}, {'date': '2005-07', 'value': 5.0}, {'date': '2005-08', 'value': 4.9}, {'date': '2005-09', 'value': 5.0}, {'date': '2005-10', 'value': 5.0}, {'date': '2005-11', 'value': 5.0}, {'date': '2005-12', 'value': 4.9}, {'date': '2006-01', 'value': 4.7}, {'date': '2006-02', 'value': 4.8}, {'date': '2006-03', 'value': 4.7}, {'date': '2006-04', 'value': 4.7}, {'date': '2006-05', 'value': 4.6}, {'date': '2006-06', 'value': 4.6}, {'date': '2006-07', 'value': 4.7}, {'date': '2006-08', 'value': 4.7}, {'date': '2006-09', 'value': 4.5}, {'date': '2006-10', 'value': 4.4}, {'date': '2006-11', 'value': 4.5}, {'date': '2006-12', 'value': 4.4}, {'date': '2007-01', 'value': 4.6}, {'date': '2007-02', 'value': 4.5}, {'date': '2007-03', 'value': 4.4}, {'date': '2007-04', 'value': 4.5}, {'date': '2007-05', 'value': 4.4}, {'date': '2007-06', 'value': 4.6}, {'date': '2007-07', 'value': 4.7}, {'date': '2007-08', 'value': 4.6}, {'date': '2007-09', 'value': 4.7}, {'date': '2007-10', 'value': 4.7}, {'date': '2007-11', 'value': 4.7}, {'date': '2007-12', 'value': 5.0}, {'date': '2008-01', 'value': 5.0}, {'date': '2008-02', 'value': 4.9}, {'date': '2008-03', 'value': 5.1}, {'date': '2008-04', 'value': 5.0}, {'date': '2008-05', 'value': 5.4}, {'date': '2008-06', 'value': 5.6}, {'date': '2008-07', 'value': 5.8}, {'date': '2008-08', 'value': 6.1}, {'date': '2008-09', 'value': 6.1}, {'date': '2008-10', 'value': 6.5}, {'date': '2008-11', 'value': 6.8}, {'date': '2008-12', 'value': 7.3}, {'date': '2009-01', 'value': 7.8}, {'date': '2009-02', 'value': 8.3}, {'date': '2009-03', 'value': 8.7}, {'date': '2009-04', 'value': 9.0}, {'date': '2009-05', 'value': 9.4}, {'date': '2009-06', 'value': 9.5}, {'date': '2009-07', 'value': 9.5}, {'date': '2009-08', 'value': 9.6}, {'date': '2009-09', 'value': 9.8}, {'date': '2009-10', 'value': 10.0}, {'date': '2009-11', 'value': 9.9}, {'date': '2009-12', 'value': 9.9}, {'date': '2010-01', 'value': 9.8}, {'date': '2010-02', 'value': 9.8}, {'date': '2010-03', 'value': 9.9}, {'date': '2010-04', 'value': 9.9}, {'date': '2010-05', 'value': 9.6}, {'date': '2010-06', 'value': 9.4}, {'date': '2010-07', 'value': 9.4}, {'date': '2010-08', 'value': 9.5}, {'date': '2010-09', 'value': 9.5}, {'date': '2010-10', 'value': 9.4}, {'date': '2010-11', 'value': 9.8}, {'date': '2010-12', 'value': 9.3}, {'date': '2011-01', 'value': 9.1}, {'date': '2011-02', 'value': 9.0}, {'date': '2011-03', 'value': 9.0}, {'date': '2011-04', 'value': 9.1}, {'date': '2011-05', 'value': 9.0}, {'date': '2011-06', 'value': 9.1}, {'date': '2011-07', 'value': 9.0}, {'date': '2011-08', 'value': 9.0}, {'date': '2011-09', 'value': 9.0}, {'date': '2011-10', 'value': 8.8}, {'date': '2011-11', 'value': 8.6}, {'date': '2011-12', 'value': 8.5}, {'date': '2012-01', 'value': 8.3}, {'date': '2012-02', 'value': 8.3}, {'date': '2012-03', 'value': 8.2}, {'date': '2012-04', 'value': 8.2}, {'date': '2012-05', 'value': 8.2}, {'date': '2012-06', 'value': 8.2}, {'date': '2012-07', 'value': 8.2}, {'date': '2012-08', 'value': 8.1}, {'date': '2012-09', 'value': 7.8}, {'date': '2012-10', 'value': 7.8}, {'date': '2012-11', 'value': 7.7}, {'date': '2012-12', 'value': 7.9}, {'date': '2013-01', 'value': 8.0}, {'date': '2013-02', 'value': 7.7}, {'date': '2013-03', 'value': 7.5}, {'date': '2013-04', 'value': 7.6}, {'date': '2013-05', 'value': 7.5}, {'date': '2013-06', 'value': 7.5}, {'date': '2013-07', 'value': 7.3}, {'date': '2013-08', 'value': 7.2}, {'date': '2013-09', 'value': 7.2}, {'date': '2013-10', 'value': 7.2}, {'date': '2013-11', 'value': 6.9}, {'date': '2013-12', 'value': 6.7}, {'date': '2014-01', 'value': 6.6}, {'date': '2014-02', 'value': 6.7}, {'date': '2014-03', 'value': 6.7}, {'date': '2014-04', 'value': 6.2}, {'date': '2014-05', 'value': 6.3}, {'date': '2014-06', 'value': 6.1}, {'date': '2014-07', 'value': 6.2}, {'date': '2014-08', 'value': 6.1}, {'date': '2014-09', 'value': 5.9}, {'date': '2014-10', 'value': 5.7}, {'date': '2014-11', 'value': 5.8}, {'date': '2014-12', 'value': 5.6}, {'date': '2015-01', 'value': 5.7}, {'date': '2015-02', 'value': 5.5}, {'date': '2015-03', 'value': 5.4}, {'date': '2015-04', 'value': 5.4}, {'date': '2015-05', 'value': 5.6}, {'date': '2015-06', 'value': 5.3}, {'date': '2015-07', 'value': 5.2}, {'date': '2015-08', 'value': 5.1}, {'date': '2015-09', 'value': 5.0}, {'date': '2015-10', 'value': 5.0}, {'date': '2015-11', 'value': 5.1}, {'date': '2015-12', 'value': 5.0}, {'date': '2016-01', 'value': 4.8}, {'date': '2016-02', 'value': 4.9}, {'date': '2016-03', 'value': 5.0}, {'date': '2016-04', 'value': 5.1}, {'date': '2016-05', 'value': 4.8}, {'date': '2016-06', 'value': 4.9}, {'date': '2016-07', 'value': 4.8}, {'date': '2016-08', 'value': 4.9}, {'date': '2016-09', 'value': 5.0}, {'date': '2016-10', 'value': 4.9}, {'date': '2016-11', 'value': 4.7}, {'date': '2016-12', 'value': 4.7}, {'date': '2017-01', 'value': 4.7}, {'date': '2017-02', 'value': 4.6}, {'date': '2017-03', 'value': 4.4}, {'date': '2017-04', 'value': 4.4}, {'date': '2017-05', 'value': 4.4}, {'date': '2017-06', 'value': 4.3}, {'date': '2017-07', 'value': 4.3}, {'date': '2017-08', 'value': 4.4}, {'date': '2017-09', 'value': 4.3}, {'date': '2017-10', 'value': 4.2}, {'date': '2017-11', 'value': 4.2}, {'date': '2017-12', 'value': 4.1}, {'date': '2018-01', 'value': 4.0}, {'date': '2018-02', 'value': 4.1}, {'date': '2018-03', 'value': 4.0}, {'date': '2018-04', 'value': 4.0}, {'date': '2018-05', 'value': 3.8}, {'date': '2018-06', 'value': 4.0}, {'date': '2018-07', 'value': 3.8}, {'date': '2018-08', 'value': 3.8}, {'date': '2018-09', 'value': 3.7}, {'date': '2018-10', 'value': 3.8}, {'date': '2018-11', 'value': 3.8}, {'date': '2018-12', 'value': 3.9}, {'date': '2019-01', 'value': 4.0}, {'date': '2019-02', 'value': 3.8}, {'date': '2019-03', 'value': 3.8}, {'date': '2019-04', 'value': 3.7}, {'date': '2019-05', 'value': 3.6}, {'date': '2019-06', 'value': 3.6}, {'date': '2019-07', 'value': 3.7}, {'date': '2019-08', 'value': 3.6}, {'date': '2019-09', 'value': 3.5}, {'date': '2019-10', 'value': 3.6}, {'date': '2019-11', 'value': 3.6}, {'date': '2019-12', 'value': 3.6}, {'date': '2020-01', 'value': 3.6}, {'date': '2020-02', 'value': 3.5}, {'date': '2020-03', 'value': 4.4}, {'date': '2020-04', 'value': 14.8}, {'date': '2020-05', 'value': 13.2}, {'date': '2020-06', 'value': 11.0}, {'date': '2020-07', 'value': 10.2}, {'date': '2020-08', 'value': 8.4}, {'date': '2020-09', 'value': 7.8}, {'date': '2020-10', 'value': 6.8}, {'date': '2020-11', 'value': 6.7}, {'date': '2020-12', 'value': 6.7}, {'date': '2021-01', 'value': 6.4}, {'date': '2021-02', 'value': 6.2}, {'date': '2021-03', 'value': 6.1}, {'date': '2021-04', 'value': 6.1}, {'date': '2021-05', 'value': 5.8}, {'date': '2021-06', 'value': 5.9}, {'date': '2021-07', 'value': 5.4}, {'date': '2021-08', 'value': 5.1}, {'date': '2021-09', 'value': 4.7}, {'date': '2021-10', 'value': 4.5}, {'date': '2021-11', 'value': 4.1}, {'date': '2021-12', 'value': 3.9}, {'date': '2022-01', 'value': 4.0}, {'date': '2022-02', 'value': 3.8}, {'date': '2022-03', 'value': 3.6}, {'date': '2022-04', 'value': 3.7}, {'date': '2022-05', 'value': 3.6}, {'date': '2022-06', 'value': 3.6}, {'date': '2022-07', 'value': 3.5}, {'date': '2022-08', 'value': 3.6}, {'date': '2022-09', 'value': 3.5}, {'date': '2022-10', 'value': 3.6}, {'date': '2022-11', 'value': 3.6}, {'date': '2022-12', 'value': 3.5}, {'date': '2023-01', 'value': 3.4}, {'date': '2023-02', 'value': 3.6}, {'date': '2023-03', 'value': 3.5}, {'date': '2023-04', 'value': 3.4}, {'date': '2023-05', 'value': 3.7}, {'date': '2023-06', 'value': 3.6}, {'date': '2023-07', 'value': 3.5}, {'date': '2023-08', 'value': 3.8}, {'date': '2023-09', 'value': 3.8}, {'date': '2023-10', 'value': 3.8}, {'date': '2023-11', 'value': 3.7}, {'date': '2023-12', 'value': 3.7}, {'date': '2024-01', 'value': 3.7}, {'date': '2024-02', 'value': 3.9}, {'date': '2024-03', 'value': 3.8}, {'date': '2024-04', 'value': 3.9}, {'date': '2024-05', 'value': 4.0}]

@st.cache_data
def get_eia_gas_price_data_statically():

    print('Not cached - EIA gas price data')
    # See https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPMR_PTE_NUS_DPG&f=M

    return [{'date': '1991-02', 'value': 1.094}, {'date': '1991-03', 'value': 1.04}, {'date': '1991-04', 'value': 1.076}, {'date': '1991-05', 'value': 1.126}, {'date': '1991-06', 'value': 1.128}, {'date': '1991-07', 'value': 1.096}, {'date': '1991-08', 'value': 1.115}, {'date': '1991-09', 'value': 1.109}, {'date': '1991-10', 'value': 1.088}, {'date': '1991-11', 'value': 1.099}, {'date': '1991-12', 'value': 1.076}, {'date': '1992-01', 'value': 1.022}, {'date': '1992-02', 'value': 1.006}, {'date': '1992-03', 'value': 1.013}, {'date': '1992-04', 'value': 1.052}, {'date': '1992-05', 'value': 1.107}, {'date': '1992-06', 'value': 1.145}, {'date': '1992-07', 'value': 1.137}, {'date': '1992-08', 'value': 1.122}, {'date': '1992-09', 'value': 1.122}, {'date': '1992-10', 'value': 1.114}, {'date': '1992-11', 'value': 1.111}, {'date': '1992-12', 'value': 1.078}, {'date': '1993-01', 'value': 1.062}, {'date': '1993-02', 'value': 1.054}, {'date': '1993-03', 'value': 1.052}, {'date': '1993-04', 'value': 1.078}, {'date': '1993-05', 'value': 1.1}, {'date': '1993-06', 'value': 1.097}, {'date': '1993-07', 'value': 1.078}, {'date': '1993-08', 'value': 1.062}, {'date': '1993-09', 'value': 1.05}, {'date': '1993-10', 'value': 1.092}, {'date': '1993-11', 'value': 1.066}, {'date': '1993-12', 'value': 1.014}, {'date': '1994-01', 'value': 0.998}, {'date': '1994-02', 'value': 1.009}, {'date': '1994-03', 'value': 1.008}, {'date': '1994-04', 'value': 1.027}, {'date': '1994-05', 'value': 1.047}, {'date': '1994-06', 'value': 1.078}, {'date': '1994-07', 'value': 1.106}, {'date': '1994-08', 'value': 1.155}, {'date': '1994-09', 'value': 1.144}, {'date': '1994-10', 'value': 1.114}, {'date': '1994-11', 'value': 1.116}, {'date': '1994-12', 'value': 1.091}, {'date': '1995-01', 'value': 1.082}, {'date': '1995-02', 'value': 1.073}, {'date': '1995-03', 'value': 1.072}, {'date': '1995-04', 'value': 1.111}, {'date': '1995-05', 'value': 1.178}, {'date': '1995-06', 'value': 1.192}, {'date': '1995-07', 'value': 1.154}, {'date': '1995-08', 'value': 1.123}, {'date': '1995-09', 'value': 1.111}, {'date': '1995-10', 'value': 1.087}, {'date': '1995-11', 'value': 1.062}, {'date': '1995-12', 'value': 1.071}, {'date': '1996-01', 'value': 1.09}, {'date': '1996-02', 'value': 1.089}, {'date': '1996-03', 'value': 1.137}, {'date': '1996-04', 'value': 1.231}, {'date': '1996-05', 'value': 1.279}, {'date': '1996-06', 'value': 1.256}, {'date': '1996-07', 'value': 1.227}, {'date': '1996-08', 'value': 1.207}, {'date': '1996-09', 'value': 1.202}, {'date': '1996-10', 'value': 1.204}, {'date': '1996-11', 'value': 1.232}, {'date': '1996-12', 'value': 1.235}, {'date': '1997-01', 'value': 1.236}, {'date': '1997-02', 'value': 1.23}, {'date': '1997-03', 'value': 1.205}, {'date': '1997-04', 'value': 1.199}, {'date': '1997-05', 'value': 1.2}, {'date': '1997-06', 'value': 1.198}, {'date': '1997-07', 'value': 1.174}, {'date': '1997-08', 'value': 1.224}, {'date': '1997-09', 'value': 1.231}, {'date': '1997-10', 'value': 1.197}, {'date': '1997-11', 'value': 1.171}, {'date': '1997-12', 'value': 1.131}, {'date': '1998-01', 'value': 1.086}, {'date': '1998-02', 'value': 1.049}, {'date': '1998-03', 'value': 1.017}, {'date': '1998-04', 'value': 1.03}, {'date': '1998-05', 'value': 1.064}, {'date': '1998-06', 'value': 1.064}, {'date': '1998-07', 'value': 1.055}, {'date': '1998-08', 'value': 1.026}, {'date': '1998-09', 'value': 1.009}, {'date': '1998-10', 'value': 1.019}, {'date': '1998-11', 'value': 0.995}, {'date': '1998-12', 'value': 0.945}, {'date': '1999-01', 'value': 0.939}, {'date': '1999-02', 'value': 0.921}, {'date': '1999-03', 'value': 0.982}, {'date': '1999-04', 'value': 1.131}, {'date': '1999-05', 'value': 1.131}, {'date': '1999-06', 'value': 1.114}, {'date': '1999-07', 'value': 1.158}, {'date': '1999-08', 'value': 1.221}, {'date': '1999-09', 'value': 1.256}, {'date': '1999-10', 'value': 1.244}, {'date': '1999-11', 'value': 1.251}, {'date': '1999-12', 'value': 1.273}, {'date': '2000-01', 'value': 1.289}, {'date': '2000-02', 'value': 1.377}, {'date': '2000-03', 'value': 1.516}, {'date': '2000-04', 'value': 1.465}, {'date': '2000-05', 'value': 1.487}, {'date': '2000-06', 'value': 1.633}, {'date': '2000-07', 'value': 1.551}, {'date': '2000-08', 'value': 1.465}, {'date': '2000-09', 'value': 1.55}, {'date': '2000-10', 'value': 1.532}, {'date': '2000-11', 'value': 1.517}, {'date': '2000-12', 'value': 1.443}, {'date': '2001-01', 'value': 1.447}, {'date': '2001-02', 'value': 1.45}, {'date': '2001-03', 'value': 1.409}, {'date': '2001-04', 'value': 1.552}, {'date': '2001-05', 'value': 1.702}, {'date': '2001-06', 'value': 1.616}, {'date': '2001-07', 'value': 1.421}, {'date': '2001-08', 'value': 1.421}, {'date': '2001-09', 'value': 1.522}, {'date': '2001-10', 'value': 1.315}, {'date': '2001-11', 'value': 1.171}, {'date': '2001-12', 'value': 1.086}, {'date': '2002-01', 'value': 1.107}, {'date': '2002-02', 'value': 1.114}, {'date': '2002-03', 'value': 1.249}, {'date': '2002-04', 'value': 1.397}, {'date': '2002-05', 'value': 1.392}, {'date': '2002-06', 'value': 1.382}, {'date': '2002-07', 'value': 1.397}, {'date': '2002-08', 'value': 1.396}, {'date': '2002-09', 'value': 1.4}, {'date': '2002-10', 'value': 1.445}, {'date': '2002-11', 'value': 1.419}, {'date': '2002-12', 'value': 1.386}, {'date': '2003-01', 'value': 1.458}, {'date': '2003-02', 'value': 1.613}, {'date': '2003-03', 'value': 1.693}, {'date': '2003-04', 'value': 1.589}, {'date': '2003-05', 'value': 1.497}, {'date': '2003-06', 'value': 1.493}, {'date': '2003-07', 'value': 1.513}, {'date': '2003-08', 'value': 1.62}, {'date': '2003-09', 'value': 1.679}, {'date': '2003-10', 'value': 1.564}, {'date': '2003-11', 'value': 1.512}, {'date': '2003-12', 'value': 1.479}, {'date': '2004-01', 'value': 1.572}, {'date': '2004-02', 'value': 1.648}, {'date': '2004-03', 'value': 1.736}, {'date': '2004-04', 'value': 1.798}, {'date': '2004-05', 'value': 1.983}, {'date': '2004-06', 'value': 1.969}, {'date': '2004-07', 'value': 1.911}, {'date': '2004-08', 'value': 1.878}, {'date': '2004-09', 'value': 1.87}, {'date': '2004-10', 'value': 2.0}, {'date': '2004-11', 'value': 1.979}, {'date': '2004-12', 'value': 1.841}, {'date': '2005-01', 'value': 1.831}, {'date': '2005-02', 'value': 1.91}, {'date': '2005-03', 'value': 2.079}, {'date': '2005-04', 'value': 2.243}, {'date': '2005-05', 'value': 2.161}, {'date': '2005-06', 'value': 2.156}, {'date': '2005-07', 'value': 2.29}, {'date': '2005-08', 'value': 2.486}, {'date': '2005-09', 'value': 2.903}, {'date': '2005-10', 'value': 2.717}, {'date': '2005-11', 'value': 2.257}, {'date': '2005-12', 'value': 2.185}, {'date': '2006-01', 'value': 2.316}, {'date': '2006-02', 'value': 2.28}, {'date': '2006-03', 'value': 2.425}, {'date': '2006-04', 'value': 2.742}, {'date': '2006-05', 'value': 2.907}, {'date': '2006-06', 'value': 2.885}, {'date': '2006-07', 'value': 2.981}, {'date': '2006-08', 'value': 2.952}, {'date': '2006-09', 'value': 2.555}, {'date': '2006-10', 'value': 2.245}, {'date': '2006-11', 'value': 2.229}, {'date': '2006-12', 'value': 2.313}, {'date': '2007-01', 'value': 2.24}, {'date': '2007-02', 'value': 2.278}, {'date': '2007-03', 'value': 2.563}, {'date': '2007-04', 'value': 2.845}, {'date': '2007-05', 'value': 3.146}, {'date': '2007-06', 'value': 3.056}, {'date': '2007-07', 'value': 2.965}, {'date': '2007-08', 'value': 2.786}, {'date': '2007-09', 'value': 2.803}, {'date': '2007-10', 'value': 2.803}, {'date': '2007-11', 'value': 3.08}, {'date': '2007-12', 'value': 3.018}, {'date': '2008-01', 'value': 3.043}, {'date': '2008-02', 'value': 3.028}, {'date': '2008-03', 'value': 3.244}, {'date': '2008-04', 'value': 3.458}, {'date': '2008-05', 'value': 3.766}, {'date': '2008-06', 'value': 4.054}, {'date': '2008-07', 'value': 4.062}, {'date': '2008-08', 'value': 3.779}, {'date': '2008-09', 'value': 3.703}, {'date': '2008-10', 'value': 3.051}, {'date': '2008-11', 'value': 2.147}, {'date': '2008-12', 'value': 1.687}, {'date': '2009-01', 'value': 1.788}, {'date': '2009-02', 'value': 1.923}, {'date': '2009-03', 'value': 1.959}, {'date': '2009-04', 'value': 2.049}, {'date': '2009-05', 'value': 2.266}, {'date': '2009-06', 'value': 2.631}, {'date': '2009-07', 'value': 2.527}, {'date': '2009-08', 'value': 2.616}, {'date': '2009-09', 'value': 2.554}, {'date': '2009-10', 'value': 2.551}, {'date': '2009-11', 'value': 2.651}, {'date': '2009-12', 'value': 2.607}, {'date': '2010-01', 'value': 2.715}, {'date': '2010-02', 'value': 2.644}, {'date': '2010-03', 'value': 2.772}, {'date': '2010-04', 'value': 2.848}, {'date': '2010-05', 'value': 2.836}, {'date': '2010-06', 'value': 2.732}, {'date': '2010-07', 'value': 2.729}, {'date': '2010-08', 'value': 2.73}, {'date': '2010-09', 'value': 2.705}, {'date': '2010-10', 'value': 2.801}, {'date': '2010-11', 'value': 2.859}, {'date': '2010-12', 'value': 2.993}, {'date': '2011-01', 'value': 3.095}, {'date': '2011-02', 'value': 3.211}, {'date': '2011-03', 'value': 3.561}, {'date': '2011-04', 'value': 3.8}, {'date': '2011-05', 'value': 3.906}, {'date': '2011-06', 'value': 3.68}, {'date': '2011-07', 'value': 3.65}, {'date': '2011-08', 'value': 3.639}, {'date': '2011-09', 'value': 3.611}, {'date': '2011-10', 'value': 3.448}, {'date': '2011-11', 'value': 3.384}, {'date': '2011-12', 'value': 3.266}, {'date': '2012-01', 'value': 3.38}, {'date': '2012-02', 'value': 3.579}, {'date': '2012-03', 'value': 3.852}, {'date': '2012-04', 'value': 3.9}, {'date': '2012-05', 'value': 3.732}, {'date': '2012-06', 'value': 3.539}, {'date': '2012-07', 'value': 3.439}, {'date': '2012-08', 'value': 3.722}, {'date': '2012-09', 'value': 3.849}, {'date': '2012-10', 'value': 3.746}, {'date': '2012-11', 'value': 3.452}, {'date': '2012-12', 'value': 3.31}, {'date': '2013-01', 'value': 3.319}, {'date': '2013-02', 'value': 3.67}, {'date': '2013-03', 'value': 3.711}, {'date': '2013-04', 'value': 3.57}, {'date': '2013-05', 'value': 3.615}, {'date': '2013-06', 'value': 3.626}, {'date': '2013-07', 'value': 3.591}, {'date': '2013-08', 'value': 3.574}, {'date': '2013-09', 'value': 3.532}, {'date': '2013-10', 'value': 3.344}, {'date': '2013-11', 'value': 3.243}, {'date': '2013-12', 'value': 3.276}, {'date': '2014-01', 'value': 3.313}, {'date': '2014-02', 'value': 3.356}, {'date': '2014-03', 'value': 3.533}, {'date': '2014-04', 'value': 3.661}, {'date': '2014-05', 'value': 3.673}, {'date': '2014-06', 'value': 3.692}, {'date': '2014-07', 'value': 3.611}, {'date': '2014-08', 'value': 3.487}, {'date': '2014-09', 'value': 3.406}, {'date': '2014-10', 'value': 3.171}, {'date': '2014-11', 'value': 2.912}, {'date': '2014-12', 'value': 2.543}, {'date': '2015-01', 'value': 2.116}, {'date': '2015-02', 'value': 2.216}, {'date': '2015-03', 'value': 2.464}, {'date': '2015-04', 'value': 2.469}, {'date': '2015-05', 'value': 2.718}, {'date': '2015-06', 'value': 2.802}, {'date': '2015-07', 'value': 2.794}, {'date': '2015-08', 'value': 2.636}, {'date': '2015-09', 'value': 2.365}, {'date': '2015-10', 'value': 2.29}, {'date': '2015-11', 'value': 2.158}, {'date': '2015-12', 'value': 2.038}, {'date': '2016-01', 'value': 1.949}, {'date': '2016-02', 'value': 1.764}, {'date': '2016-03', 'value': 1.969}, {'date': '2016-04', 'value': 2.113}, {'date': '2016-05', 'value': 2.268}, {'date': '2016-06', 'value': 2.366}, {'date': '2016-07', 'value': 2.239}, {'date': '2016-08', 'value': 2.178}, {'date': '2016-09', 'value': 2.219}, {'date': '2016-10', 'value': 2.249}, {'date': '2016-11', 'value': 2.182}, {'date': '2016-12', 'value': 2.254}, {'date': '2017-01', 'value': 2.349}, {'date': '2017-02', 'value': 2.304}, {'date': '2017-03', 'value': 2.325}, {'date': '2017-04', 'value': 2.417}, {'date': '2017-05', 'value': 2.391}, {'date': '2017-06', 'value': 2.347}, {'date': '2017-07', 'value': 2.3}, {'date': '2017-08', 'value': 2.38}, {'date': '2017-09', 'value': 2.645}, {'date': '2017-10', 'value': 2.505}, {'date': '2017-11', 'value': 2.564}, {'date': '2017-12', 'value': 2.477}, {'date': '2018-01', 'value': 2.555}, {'date': '2018-02', 'value': 2.587}, {'date': '2018-03', 'value': 2.591}, {'date': '2018-04', 'value': 2.757}, {'date': '2018-05', 'value': 2.901}, {'date': '2018-06', 'value': 2.891}, {'date': '2018-07', 'value': 2.849}, {'date': '2018-08', 'value': 2.836}, {'date': '2018-09', 'value': 2.836}, {'date': '2018-10', 'value': 2.86}, {'date': '2018-11', 'value': 2.647}, {'date': '2018-12', 'value': 2.366}, {'date': '2019-01', 'value': 2.248}, {'date': '2019-02', 'value': 2.309}, {'date': '2019-03', 'value': 2.516}, {'date': '2019-04', 'value': 2.798}, {'date': '2019-05', 'value': 2.859}, {'date': '2019-06', 'value': 2.716}, {'date': '2019-07', 'value': 2.74}, {'date': '2019-08', 'value': 2.621}, {'date': '2019-09', 'value': 2.592}, {'date': '2019-10', 'value': 2.627}, {'date': '2019-11', 'value': 2.598}, {'date': '2019-12', 'value': 2.555}, {'date': '2020-01', 'value': 2.548}, {'date': '2020-02', 'value': 2.442}, {'date': '2020-03', 'value': 2.234}, {'date': '2020-04', 'value': 1.841}, {'date': '2020-05', 'value': 1.87}, {'date': '2020-06', 'value': 2.082}, {'date': '2020-07', 'value': 2.183}, {'date': '2020-08', 'value': 2.182}, {'date': '2020-09', 'value': 2.183}, {'date': '2020-10', 'value': 2.158}, {'date': '2020-11', 'value': 2.108}, {'date': '2020-12', 'value': 2.195}, {'date': '2021-01', 'value': 2.334}, {'date': '2021-02', 'value': 2.501}, {'date': '2021-03', 'value': 2.81}, {'date': '2021-04', 'value': 2.858}, {'date': '2021-05', 'value': 2.985}, {'date': '2021-06', 'value': 3.064}, {'date': '2021-07', 'value': 3.136}, {'date': '2021-08', 'value': 3.158}, {'date': '2021-09', 'value': 3.175}, {'date': '2021-10', 'value': 3.291}, {'date': '2021-11', 'value': 3.395}, {'date': '2021-12', 'value': 3.307}, {'date': '2022-01', 'value': 3.315}, {'date': '2022-02', 'value': 3.517}, {'date': '2022-03', 'value': 4.222}, {'date': '2022-04', 'value': 4.109}, {'date': '2022-05', 'value': 4.444}, {'date': '2022-06', 'value': 4.929}, {'date': '2022-07', 'value': 4.559}, {'date': '2022-08', 'value': 3.975}, {'date': '2022-09', 'value': 3.7}, {'date': '2022-10', 'value': 3.815}, {'date': '2022-11', 'value': 3.685}, {'date': '2022-12', 'value': 3.21}, {'date': '2023-01', 'value': 3.339}, {'date': '2023-02', 'value': 3.389}, {'date': '2023-03', 'value': 3.422}, {'date': '2023-04', 'value': 3.603}, {'date': '2023-05', 'value': 3.555}, {'date': '2023-06', 'value': 3.571}, {'date': '2023-07', 'value': 3.597}, {'date': '2023-08', 'value': 3.84}, {'date': '2023-09', 'value': 3.836}, {'date': '2023-10', 'value': 3.613}, {'date': '2023-11', 'value': 3.318}, {'date': '2023-12', 'value': 3.134}, {'date': '2024-01', 'value': 3.075}, {'date': '2024-02', 'value': 3.212}, {'date': '2024-03', 'value': 3.426}, {'date': '2024-04', 'value': 3.611}, {'date': '2024-05', 'value': 3.603}]

@st.cache_data
def get_predictit_prices():

    print('Not cached - PredictIt data')

    response = requests.get('https://www.predictit.org/api/Public/GetMarketChartData/7456?timespan=90&maxContracts=6&isTimespanInHours=false').json()
    cleaned_up_response = [{'date': x['dateString'], 'value': x['closeSharePrice']} for x in response if x['contractName'] == 'Biden']
    return cleaned_up_response

@st.cache_data
def get_fed_funds_rate_data():

    print('Not cached - Fed funds data')

    fed_funds = requests.get(f'https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={os.environ.get("FRED_API_KEY")}&file_type=json').json()
    list_data = [{'date': "-".join(x['date'].split("-")[:-1]), 'value': float(x['value']) } for x in fed_funds['observations']]
    return list_data

@st.cache_data
def get_gdp_growth_data():

    df = pd.read_excel('https://cdn.ihsmarkit.com/www/default/1020/US-Monthly-GDP-History-Data.xlsx', sheet_name='Data', header=0)
    df = df.rename(columns={'Unnamed: 0': 'date', 'Monthly Real GDP Index': 'value'})
    df = df[["date", "value"]]
    df = df[(df["date"] != '') & (df["date"].isnull() == False)]
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(str(x).strip().split(' - ')[0] + ' - ' + str(x).strip().split(' - ')[1][:3], '%Y - %b').strftime('%Y-%m'))
    # st.write('Raw data')
    # df
    return df.to_dict(orient='records')

######
## The below section includes various utility and data manipulation functions
######

# For example, FRBSF measures news sentiment daily, but we may want to average all values in a month if the dependent variable we're testing against (e.g. UMich consumer sentiment) is only available monthly.
def average_daily_data_over_interval(data, strftime_interval):
    
    dict_data = {}
    for datum in data:
        if datetime.datetime.strptime(datum['date'], '%Y-%m-%d').strftime(strftime_interval) not in dict_data:
            dict_data[datetime.datetime.strptime(datum['date'], '%Y-%m-%d').strftime(strftime_interval)] = []
        dict_data[datetime.datetime.strptime(datum['date'], '%Y-%m-%d').strftime(strftime_interval)].append(datum['value'])

    list_data = []
    for date_str, value in dict_data.items():
        list_data.append({
            'date': date_str,
            'value': sum(value)/len(value)
        })
    
    return list_data

# Automatically infer which level of specificity a specific dataset has (e.g. it's daily as in 2023-10-01, or monthly as in 2023-10).
def detect_date_strftime_setting(date_string):

    if len(date_string.split('-')) == 3:
        return '%Y-%m-%d'
    elif len(date_string.split('-')) == 2:
        return '%Y-%m'
    
# For example, we may want to measure lagging effects, e.g. the effect of the unemployment rate as of 3 months ago (not today) on consumer sentiment today.
def time_shift_the_data(data, interval, number_of_intervals):
    strftime_setting = detect_date_strftime_setting(data[0]['date'])
    if interval == 'days':
        return [{'date': (datetime.datetime.strptime(x['date'], strftime_setting) + pd.DateOffset(days=number_of_intervals)).strftime(strftime_setting), 'value': x['value']} for x in data]
    else:
        return [{'date': (datetime.datetime.strptime(x['date'], strftime_setting) + pd.DateOffset(months=number_of_intervals)).strftime(strftime_setting), 'value': x['value']} for x in data]

# For example, inflation data is represented as a monthly price level number (CPI-U). To calculate inflation, you need to calculate the change in that number over some period of time. 
def transform_data_into_annual_rate_of_change(data, calc_method='same_month_last_year'):

    list_data = []
    strftime_setting = detect_date_strftime_setting(data[0]['date'])
    for data_point in data:

        if calc_method == 'same_month_last_year':
            baseline_date = (datetime.datetime.strptime(data_point['date'], strftime_setting) - pd.DateOffset(years=1)).strftime(strftime_setting)
        elif calc_method == 'monthly_annualized':
            baseline_date = (datetime.datetime.strptime(data_point['date'], strftime_setting) - pd.DateOffset(months=1)).strftime(strftime_setting)
        matching_data_point = next((x for x in data if x['date'] == baseline_date), None)
        if matching_data_point is None:
            continue

        if calc_method == 'same_month_last_year':
            this_value = (data_point['value'] - matching_data_point['value']) / matching_data_point['value'] * 100
        elif calc_method == 'monthly_annualized':
            this_value = (((data_point['value'] / matching_data_point['value']) ** 12) - 1) * 100

        list_data.append({
            'date': data_point['date'],
            'value': this_value
        })
    
    return list_data
    
# Takes an arbitrary number of datasets and returns a list of *values* from those same datasets, but only for the dates for which all datasets have data points
def align_datasets(*datasets, include_dates=False):

    list_data = [ [] for x in datasets]
    for data_point in datasets[0]: # Use the first dataset as the baseline to check for date alignment
        data_points_for_this_date = []
        for dataset in datasets:
            matching_data_record = next((y for y in dataset if y['date'] == data_point['date']), None)
            if matching_data_record is None:
                break
            data_points_for_this_date.append(matching_data_record)
        if len(data_points_for_this_date) == len(datasets):
            for idx, _ in enumerate(datasets):
                if include_dates:
                    list_data[idx].append(data_points_for_this_date[idx])
                else:
                    list_data[idx].append(data_points_for_this_date[idx]['value'])

    return list_data

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def run_app():

    eligible_datasets = [
        {
            'title': 'University of Michigan Index of Consumer Sentiment',
            'short_title': 'UMich Consumer Sentiment',
            'url': 'http://www.sca.isr.umich.edu/',
            'cadence': 'monthly'
            # 'description': 'The Index of Consumer Sentiment'
        },
        {
            'title': 'University of Michigan Index of Consumer Expectations',
            'short_title': 'UMich Consumer Expectations',
            'url': 'http://www.sca.isr.umich.edu/',
            'cadence': 'monthly'
        },
        {
            'title': 'University of Michigan Index of Current Economic Conditions',
            'short_title': 'UMich Current Economic Conditions',
            'url': 'http://www.sca.isr.umich.edu/',
            'cadence': 'monthly'
        },
        {
            'title': 'Conference Board Consumer Confidence Index',
            'short_title': 'Conf. Board Consumer Confidence',
            'url': 'https://www.conference-board.org/topics/consumer-confidence',
            'cadence': 'monthly'
        },
        {
            'title': 'Civiqs National Economy Current Condition - Net Good',
            'short_title': 'Civiqs Economic Sentiment',
            'url': 'https://civiqs.com/results/economy_us_now?uncertainty=true&annotations=true&zoomIn=true&net=true',
            'cadence': 'daily'
        },
        {
            'title': 'A Democrat is President of the United States',
            'short_title': 'Democrat is U.S. President',
            'url': 'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States',
            'cadence': 'daily'
        },
        {
            'title': 'Federal Reserve Bank of San Francisco Daily News Sentiment Index',
            'short_title': 'FRBSF Daily News Sentiment',
            'url': 'https://www.frbsf.org/research-and-insights/data-and-indicators/daily-news-sentiment-index/',
            'cadence': 'daily'
        },
        # {
        #     'title': 'GasBuddy Daily National Gas Prices',
        #     'short_title': 'National Gas Prices',
        #     'url': 'https://fuelinsights.gasbuddy.com/charts',
        #     'cadence': 'daily'
        # },
        {
            'title': 'Civiqs Joe Biden Job Approval - Net Approve',
            'short_title': 'Civiqs Joe Biden Job Approval',
            'url': 'https://civiqs.com/results/approve_president_biden?uncertainty=true&annotations=true&zoomIn=true&net=true',
            'cadence': 'daily'
        },
        {
            'title': '538 Joe Biden 2024 Election Polling Average',
            'short_title': 'Biden 2024 Polling Avg',
            'url': 'https://projects.fivethirtyeight.com/polls/president-general/2024/national/',
            'cadence': 'daily'
        },
        {
            'title': 'Bureau of Labor Statistics Annual CPI Inflation Rate',
            'short_title': 'Inflation Rate',
            'url': 'https://data.bls.gov/cgi-bin/surveymost?cu',
            'cadence': 'monthly'
        },
        {
            'title': 'Bureau of Labor Statistics Unemployment Rate',
            'short_title': 'Unemployment Rate',
            'url': 'https://data.bls.gov/cgi-bin/surveymost?ln',
            'cadence': 'monthly'
        },
        {
            'title': 'U.S. Energy Information Administration Monthly Retail Gas Prices',
            'short_title': 'National Gas Prices',
            'url': 'https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPMR_PTE_NUS_DPG&f=M',
            'cadence': 'monthly'
        },
        {
            'title': 'PredictIt Odds of Biden 2024 Victory',
            'short_title': 'PredictIt Biden Odds',
            'url': 'https://www.predictit.org/markets/detail/7456/Who-will-win-the-2024-US-presidential-election',
            'cadence': 'daily'
        },
        {
            'title': 'Federal Funds Effective Rate',
            'short_title': 'Fed Funds Rate',
            'url': 'https://fred.stlouisfed.org/series/FEDFUNDS',
            'cadence': 'monthly'
        },
        {
            'title': 'S&P GMI GDP Growth Rate',
            'short_title': 'GDP Growth Rate',
            'url': 'https://www.spglobal.com/marketintelligence/en/mi/products/us-monthly-gdp-index.html',
            'cadence': 'monthly',
            'description': 'The GDP growth rate is calculated here by annualizing the change in estimated monthly GDP. See https://cdn.ihsmarkit.com/www/pdf/1020/US-Monthly-GDP-Current-Index.pdf for examples.'
        }
    ]

    if 'run_correlation_automatically' not in st.session_state:
        st.session_state['run_correlation_automatically'] = True

    st.header("Correlation Explorer")

    # See https://st-experimental-fragment.streamlit.app/Dynamic_form
    @st.experimental_fragment
    def fragment_form(eligible_datasets):

        print('Just started fragment')
        print(list(st.session_state.keys()))

        # st.session_state.custom_dataset_1 = None
        # st.session_state.custom_dataset_2 = None

        st.selectbox('Pick dataset #1', [x['title'] for x in eligible_datasets] + ['Upload my own dataset'], index=0, key='dataset1_picker', help=None, on_change=None, args=None, kwargs=None, placeholder="Choose an option", disabled=False, label_visibility="visible")
        st.caption(next((x['url'] for x in eligible_datasets if st.session_state.dataset1_picker == x['title']), ''))
        st.caption(next((x['description'] for x in eligible_datasets if 'description' in x and st.session_state.dataset1_picker == x['title']), ''))

        if st.session_state.dataset1_picker == 'Upload my own dataset':
            st.file_uploader('Upload a CSV with two columns: "date" (YYYY-MM-DD or YYYY-MM) and "value" (int or float)', type=['csv'], accept_multiple_files=False, key='custom_dataset_picker_1', help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

        st.selectbox('Pick dataset #2', [x['title'] for x in eligible_datasets] + ['Upload my own dataset'], index=3, key='dataset2_picker', help=None, on_change=None, args=None, kwargs=None, placeholder="Choose an option", disabled=False, label_visibility="visible")
        st.caption(next((x['url'] for x in eligible_datasets if st.session_state.dataset2_picker == x['title']), ''))
        st.caption(next((x['description'] for x in eligible_datasets if 'description' in x and st.session_state.dataset2_picker == x['title']), ''))

        if st.session_state.dataset2_picker == 'Upload my own dataset':
            st.file_uploader('Upload a CSV with two columns: "date" (YYYY-MM-DD or YYYY-MM) and "value" (int or float)', type=['csv'], accept_multiple_files=False, key='custom_dataset_picker_2', help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

        # Below is what happens when you click on the `Correlate datasets` button
        if st.button(label='Correlate datasets', type='primary', key='submit_btn'):

            print('Just pushed button')

            if st.session_state.dataset1_picker == 'Upload my own dataset':

                temp_dataset = pd.read_csv(st.session_state.custom_dataset_picker_1, header=0, usecols=['date', 'value'], index_col=False).to_dict(orient='records')
                st.session_state.custom_dataset_1 = {
                    'dataset': temp_dataset,
                    'title': 'Custom Dataset 1',
                    'short_title': 'Custom Dataset 1',
                    'url': None,
                    'cadence': 'monthly' if detect_date_strftime_setting(temp_dataset[0]['date']) == '%Y-%m' else 'daily'
                }

            if st.session_state.dataset2_picker == 'Upload my own dataset':

                temp_dataset = pd.read_csv(st.session_state.custom_dataset_picker_2, header=0, usecols=['date', 'value'], index_col=False).to_dict(orient='records')
                st.session_state.custom_dataset_2 = {
                    'dataset': temp_dataset,
                    'title': 'Custom Dataset 2',
                    'short_title': 'Custom Dataset 2',
                    'url': None,
                    'cadence': 'monthly' if detect_date_strftime_setting(temp_dataset[0]['date']) == '%Y-%m' else 'daily'
                }

            st.session_state.dataset1 = next((x for x in eligible_datasets if x['title'] == st.session_state.dataset1_picker), None) if st.session_state.custom_dataset_1 is None else st.session_state.custom_dataset_1
            st.session_state.dataset2 = next((x for x in eligible_datasets if x['title'] == st.session_state.dataset2_picker), None) if st.session_state.custom_dataset_2 is None else st.session_state.custom_dataset_2
            st.session_state.comparison_cadence = '%Y-%m' if st.session_state.dataset1['cadence'] != st.session_state.dataset2['cadence'] or st.session_state.dataset1['cadence'] == 'monthly' else '%Y-%m-%d'

            st.session_state.form_submitted = True

            print('Got to end of fragment, about to rerun()')
            print(list(st.session_state.keys()))

            st.rerun()

    fragment_form(eligible_datasets=eligible_datasets)

    if 'form_submitted' not in st.session_state:
        st.session_state['form_submitted'] = False

    # Set defaults - the comparison cadence defaults to monthly because by default we're comparing two monthly datasets (UMich ICS and Conf. Board Consumer Confidence)
    if st.session_state.form_submitted == False:
        print('Form has not been submitted')
        st.session_state.comparison_cadence = '%Y-%m'
        st.session_state.dataset1 = next((x for x in eligible_datasets if x['title'] == st.session_state.dataset1_picker), None)
        st.session_state.dataset2 = next((x for x in eligible_datasets if x['title'] == st.session_state.dataset2_picker), None)
        st.session_state.custom_dataset_1 = None
        st.session_state.custom_dataset_2 = None

    if st.session_state.form_submitted or st.session_state.run_correlation_automatically:

        del st.session_state['run_correlation_automatically']

        dataset_candidates = []

        st.slider(label=f"Shift each observation in dataset #2 backwards by the below number of {'days' if st.session_state.comparison_cadence == '%Y-%m-%d' else 'months'} before comparing datasets (see methodology section below)", min_value=0, max_value=365 if st.session_state.comparison_cadence == '%Y-%m-%d' else 12, value=0, key='dataset2_lag')

        with st.spinner('Loading datasets...'):
            for dataset_index in [1, 2]:

                if dataset_index == 1:
                    dataset_value = st.session_state.dataset1_picker
                else:
                    dataset_value = st.session_state.dataset2_picker

                revised_dataset = None

                # Monthly indicators
                if dataset_value == 'University of Michigan Index of Consumer Sentiment':
                    revised_dataset = get_umich_data(series='ics')
                elif dataset_value == 'University of Michigan Index of Consumer Expectations':
                    revised_dataset = get_umich_data(series='ice')
                elif dataset_value == 'University of Michigan Index of Current Economic Conditions':
                    revised_dataset = get_umich_data(series='icc')
                elif dataset_value == 'Conference Board Consumer Confidence Index':
                    revised_dataset = get_conference_board_leading_indicators_data(exact_date=False)
                elif dataset_value == 'Bureau of Labor Statistics Annual CPI Inflation Rate':
                    # dataset_candidates.append(transform_data_into_annual_rate_of_change(get_bls_data(series='inflation')))
                    revised_dataset = transform_data_into_annual_rate_of_change(get_bls_inflation_data_statically())
                elif dataset_value == 'Bureau of Labor Statistics Unemployment Rate':
                    # dataset_candidates.append(transform_data_into_annual_rate_of_change(get_bls_data(series='unemployment')))
                    revised_dataset = get_bls_unemployment_data_statically()
                elif dataset_value == 'U.S. Energy Information Administration Monthly Retail Gas Prices':
                    revised_dataset = get_eia_gas_price_data_statically()
                elif dataset_value == 'Federal Funds Effective Rate':
                    revised_dataset = get_fed_funds_rate_data()
                elif dataset_value == 'S&P GMI GDP Growth Rate':
                    trailing_avg = get_gdp_growth_data()
                    # st.write(pd.DataFrame(trailing_avg))
                    revised_dataset = transform_data_into_annual_rate_of_change(trailing_avg, calc_method='monthly_annualized')
                    # st.write(pd.DataFrame(revised_dataset))

                # Potentially daily indicators
                elif dataset_value == 'Civiqs National Economy Current Condition - Net Good':
                    revised_dataset = get_civiqs_sentiment_data()
                elif dataset_value == 'A Democrat is President of the United States':
                    revised_dataset = get_democrat_in_white_house_data()
                elif dataset_value == 'Federal Reserve Bank of San Francisco Daily News Sentiment Index':
                    revised_dataset = get_frb_news_sentiment_data()
                # elif dataset_value == 'GasBuddy Daily National Gas Prices':
                #     revised_dataset = get_gasbuddy_prices()
                elif dataset_value == 'Civiqs Joe Biden Job Approval - Net Approve':
                    revised_dataset = get_civiqs_biden_job_approval_data()
                elif dataset_value == '538 Joe Biden 2024 Election Polling Average':
                    revised_dataset = get_joe_biden_polling_average()
                elif dataset_value == 'PredictIt Odds of Biden 2024 Victory':
                    revised_dataset = get_predictit_prices()

                # Custom datasets
                elif st.session_state.custom_dataset_1 is not None and dataset_index == 1:
                    revised_dataset = st.session_state.custom_dataset_1['dataset']
                elif st.session_state.custom_dataset_2 is not None and dataset_index == 2:
                    revised_dataset = st.session_state.custom_dataset_2['dataset']


                if dataset_index == 2 and st.session_state.dataset2_lag > 0:
                    revised_dataset = time_shift_the_data(revised_dataset, 'days' if st.session_state.comparison_cadence == '%Y-%m-%d' else 'months', st.session_state.dataset2_lag)

                if st.session_state.dataset1['cadence'] == 'daily' and st.session_state.comparison_cadence == '%Y-%m' and dataset_index == 1:
                    dataset_candidates.append(average_daily_data_over_interval(revised_dataset, '%Y-%m'))
                elif st.session_state.comparison_cadence == '%Y-%m' and st.session_state.dataset2['cadence'] == 'daily' and dataset_index == 2:
                    dataset_candidates.append(average_daily_data_over_interval(revised_dataset, '%Y-%m'))
                else:
                    dataset_candidates.append(revised_dataset)

        datasets = align_datasets(dataset_candidates[0], dataset_candidates[1], include_dates=True)

        min_date = sorted(datasets[0], key = lambda x: x['date'])[0]['date']
        max_date = sorted(datasets[0], key = lambda x: x['date'], reverse=True)[0]['date']

        min_date = datetime.datetime.strptime(min_date, st.session_state.comparison_cadence)
        max_date = datetime.datetime.strptime(max_date, st.session_state.comparison_cadence)

        if 'date_filter' in st.session_state:
            print(st.session_state.date_filter)
        else:
            print('no date filter in session_state')
        st.slider(
            "Limit observations to a custom date range",
            value=(min_date, max_date) if 'date_filter' not in st.session_state or st.session_state.form_submitted else (max(min_date, st.session_state.date_filter[0]), min(max_date, st.session_state.date_filter[1])),
            min_value=min_date,
            max_value=max_date,
            format="YYYY-MM-DD",
            key='date_filter'
        )

        del st.session_state['form_submitted']

        datasets[0] = [x for x in datasets[0] if datetime.datetime.strptime(x['date'], st.session_state.comparison_cadence) >= st.session_state.date_filter[0] and datetime.datetime.strptime(x['date'], st.session_state.comparison_cadence) <= st.session_state.date_filter[1]]
        datasets[1] = [x for x in datasets[1] if datetime.datetime.strptime(x['date'], st.session_state.comparison_cadence) >= st.session_state.date_filter[0] and datetime.datetime.strptime(x['date'], st.session_state.comparison_cadence) <= st.session_state.date_filter[1]]

        if len(datasets[0]) >= 4:

            pearsons_r = calculate_pearsons([x['value'] for x in datasets[0]], [x['value'] for x in datasets[1]])

            st.metric(label="Pearson's r", value=round(pearsons_r, 3), delta="Strong" if abs(pearsons_r) >= 0.6 else "Moderate" if abs(pearsons_r) >= 0.4 else "Weak")

            st.metric(label="Observations", value=f'{len(datasets[0]):,}')

            dataset1_df = pd.DataFrame(datasets[0])
            dataset1_df = dataset1_df.rename(columns={"value": 'data1'})
            dataset2_df = pd.DataFrame(datasets[1])
            dataset2_df = dataset2_df.rename(columns={"value": 'data2'})

            chart_df = dataset1_df.join(dataset2_df.set_index('date'), on='date')

            if st.session_state.dataset1_picker != st.session_state.dataset2_picker:
                table_df = chart_df.rename(columns={'data1': st.session_state.dataset1_picker, 'data2': st.session_state.dataset2_picker})
                table_df = table_df[['date', st.session_state.dataset1_picker, st.session_state.dataset2_picker]]
            else:
                table_df = chart_df.rename(columns={'data1': f'1 - {st.session_state.dataset1_picker}', 'data2': f'2 - {st.session_state.dataset2_picker}'})
                table_df = table_df[['date', f'1 - {st.session_state.dataset1_picker}', f'2 - {st.session_state.dataset2_picker}']]

            dataset1_short_title = next((x['short_title'] for x in eligible_datasets if st.session_state.dataset1_picker == x['title']), None) if st.session_state.custom_dataset_1 is None else st.session_state.custom_dataset_1['short_title']
            dataset2_short_title = next((x['short_title'] for x in eligible_datasets if st.session_state.dataset2_picker == x['title']), None) if st.session_state.custom_dataset_2 is None else st.session_state.custom_dataset_2['short_title']

            # Taken from https://stackoverflow.com/q/70117272 
            base = alt.Chart(chart_df, height=500).encode(x=alt.X('date', axis=alt.Axis(labelAngle=325)))
            line =  base.mark_line(color='red').encode(y=alt.Y('data1:Q', axis=alt.Axis(grid=True, titleColor='red'), scale=alt.Scale(zero=False)).title(dataset1_short_title))
            line2 = base.mark_line(color='blue').encode(y=alt.Y('data2:Q', axis=alt.Axis(titleColor='blue'), scale=alt.Scale(zero=False)).title(dataset2_short_title))
            c = (line + line2).resolve_scale(y='independent').properties(width=600)
            st.altair_chart(c, use_container_width=True)

            with st.expander("See raw data"):
                table_df

        else:

            st.write('**Not enough data observations in common between these two datasets to calculate a meaningful correlation.** Try another combination of datasets.')


    with st.expander("See methodology"):
        st.write('''
            Each dataset above is available for free publicly at the URLs below the selection boxes.
                
            The Pearson's r coefficient is a measure of the strength of correlation between two data series. (Note that Pearson's r does *not* tell us the direction of *causation* between the two datasets or even whether any exists at all, but simply the degree to which the two datasets are correlated.)
                
            The value of Pearson's r ranges from a minimum of -1 to a maximum of 1. A value of 1 represents perfect positive correlation while a value of -1 represents perfect negative correlation. A Pearson's r value of 0 indicates that there is no relationship whatsoever between the two datasets.
                
            In practice, no two datasets will ever be perfectly correlated or perfectly uncorrelated. Although no exact consensus exists on the threshold of 'strong' correlation, generally a Pearson's r coefficient of 0.6 or above (or -0.6 or below) is considered a strong correlation.
                
            An important detail about the Pearson's r metric is that it requires two datasets of exactly equal length. That is, a monthly dataset covering two years cannot be compared to a monthly dataset that covers only one. This presents a challenge given the variety of datasets available here.
                
            To acccount for this, I have made two key adjustments to the datasets.
                
            First, I only include the data points from *dates in common* between the two datasets being compared. For example, when comparing a monthly dataset with observations from June 2019 to May 2023 with another dataset running from August 2001 to February 2024, I will trim both datasets so they only include observations between August 2001 and May 2023, a period during which both datasets have observations. (You can further limit the date range using the slider.)
                
            Secondly, when comparing two datasets whose observations occur at *different cadences* - e.g., one is reported monthly and the other is reported daily - I average the higher-frequency dataset over the lower-frequency cadence. An example of this would be correlating average gas prices (a dataset with daily observations) to consumer sentiment indices (which are generally measured monthly): in this case, I first average the daily gas prices for each month before correlating them with the monthly consumer sentiment index dataset.
                
            Additionally, you can time-shift the second dataset up to 365 days or 12 months back in time (depending on whether the correlation is being calculated on a daily or monthly basis, respectively). This allows you to measure correlations for lagging indicators: for example, it is possible that today's consumer sentiment correlates more closely with gas prices from 3 months ago rather than their current price right now.
                
            The line chart, and the data table directly above it, represent these datasets *after* all of these adjustments are made. (You can export/download the data to check it yourself and conduct your own analyses.) If you see any errors or bugs, please let me know!
        ''')

    html('''
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        <a href="https://twitter.com/jaypinho?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-size="large" data-show-count="false">Follow @jaypinho</a>
        <br>
        <a href="https://www.buymeacoffee.com/tether" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" ></a>
    ''')

    st.write('''
        <p>
            Correlations Explorer is brought to you by <a href="https://twitter.com/jaypinho" target="_blank">Jay Pinho</a>.
        </p>
        <p>
            Previous projects include:
            <ul>
                <li><a href="https://transcripts.streamlit.app/" target="_blank">Transcript Accuracy Analyzer</a></li>
                <li><a href="https://podcast.streamlit.app/" target="_blank">Podcast Summarizer</a></li>
                <li><a href="https://www.tethertransparency.com/" target="_blank">Tether Insolvency Calculator</a></li>
                <li><a href="http://www.fedproject.com/" target="_blank">The Fed Project</a></li>
                <li><a href="https://www.scotusmap.com/" target="_blank">SCOTUS Map</a></li>
            </ul>
        </p>
        <p>
            Subscribe to <a href="https://networked.substack.com/" target="_blank">my technology and politics newsletter</a>.
        </p>
        <p>
            See any mistakes? <a href="https://twitter.com/jaypinho" target="_blank">Let me know</a>.
        </p>
    ''', unsafe_allow_html=True)


run_app()