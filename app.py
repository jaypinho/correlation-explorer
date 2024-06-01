import streamlit as st
import numpy as np
import pandas as pd
import requests
import io
import datetime
import altair as alt
from streamlit.components.v1 import html

def calculate_pearsons(series1, series2):
    return np.corrcoef(series1, series2)[0, 1]

def get_umich_data(series='ics'):

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

def get_conference_board_leading_indicators_data(exact_date=True):

    # From https://www.investing.com/economic-calendar/cb-consumer-confidence-48

    # Run this on the page:

    # y = [];
    # for (i=1; i < x.querySelectorAll('tbody tr').length; i++) {
    #     if (x.querySelectorAll('tbody tr')[i].getElementsByTagName('td')[0].innerText == 'Jan 01, 2008 (Dec)') {break;}
    #     y.push({'date': x.querySelectorAll('tbody tr')[i].getElementsByTagName('td')[0].innerText.split(" (")[0], 'value': parseFloat(x.querySelectorAll('tbody tr')[i-1].getElementsByTagName('td')[4].innerText)});
    # }

    data_series = [{'date': '2008-02-26', 'value': 75.0}, {'date': '2008-03-25', 'value': 64.5}, {'date': '2008-04-29', 'value': 62.3}, {'date': '2008-05-27', 'value': 57.2}, {'date': '2008-06-24', 'value': 50.4}, {'date': '2008-07-29', 'value': 51.9}, {'date': '2008-08-26', 'value': 56.9}, {'date': '2008-09-30', 'value': 59.8}, {'date': '2008-10-28', 'value': 38.0}, {'date': '2008-11-25', 'value': 44.9}, {'date': '2008-12-30', 'value': 38.0}, {'date': '2009-01-27', 'value': 37.7}, {'date': '2009-02-24', 'value': 25.0}, {'date': '2009-03-31', 'value': 26.9}, {'date': '2009-04-28', 'value': 40.8}, {'date': '2009-05-26', 'value': 54.8}, {'date': '2009-06-30', 'value': 49.3}, {'date': '2009-07-28', 'value': 47.4}, {'date': '2009-08-25', 'value': 54.5}, {'date': '2009-09-29', 'value': 53.4}, {'date': '2009-10-27', 'value': 48.7}, {'date': '2009-11-24', 'value': 50.6}, {'date': '2009-12-29', 'value': 53.6}, {'date': '2010-01-26', 'value': 56.5}, {'date': '2010-02-23', 'value': 46.4}, {'date': '2010-03-30', 'value': 52.3}, {'date': '2010-04-27', 'value': 57.7}, {'date': '2010-05-25', 'value': 62.7}, {'date': '2010-06-29', 'value': 54.3}, {'date': '2010-07-27', 'value': 51.0}, {'date': '2010-08-31', 'value': 53.2}, {'date': '2010-09-28', 'value': 48.6}, {'date': '2010-10-26', 'value': 49.9}, {'date': '2010-11-30', 'value': 54.3}, {'date': '2010-12-28', 'value': 53.3}, {'date': '2011-01-25', 'value': 64.8}, {'date': '2011-02-22', 'value': 72.0}, {'date': '2011-03-29', 'value': 63.8}, {'date': '2011-04-26', 'value': 66.0}, {'date': '2011-05-31', 'value': 61.7}, {'date': '2011-06-28', 'value': 57.6}, {'date': '2011-07-26', 'value': 59.2}, {'date': '2011-08-30', 'value': 45.2}, {'date': '2011-09-27', 'value': 46.4}, {'date': '2011-10-25', 'value': 40.9}, {'date': '2011-11-29', 'value': 55.2}, {'date': '2011-12-27', 'value': 64.8}, {'date': '2012-01-31', 'value': 61.5}, {'date': '2012-02-28', 'value': 71.6}, {'date': '2012-03-27', 'value': 69.5}, {'date': '2012-04-24', 'value': 68.7}, {'date': '2012-05-29', 'value': 64.4}, {'date': '2012-06-26', 'value': 62.7}, {'date': '2012-07-31', 'value': 65.4}, {'date': '2012-08-28', 'value': 61.3}, {'date': '2012-09-25', 'value': 68.4}, {'date': '2012-11-01', 'value': 73.1}, {'date': '2012-11-27', 'value': 71.5}, {'date': '2012-12-27', 'value': 66.7}, {'date': '2013-01-29', 'value': 58.4}, {'date': '2013-02-26', 'value': 68.0}, {'date': '2013-03-26', 'value': 61.9}, {'date': '2013-04-30', 'value': 69.0}, {'date': '2013-05-28', 'value': 74.3}, {'date': '2013-06-25', 'value': 82.1}, {'date': '2013-07-30', 'value': 81.0}, {'date': '2013-08-27', 'value': 81.8}, {'date': '2013-09-24', 'value': 80.2}, {'date': '2013-10-29', 'value': 72.4}, {'date': '2013-11-26', 'value': 72.0}, {'date': '2013-12-31', 'value': 77.5}, {'date': '2014-01-28', 'value': 79.4}, {'date': '2014-02-25', 'value': 78.3}, {'date': '2014-03-25', 'value': 83.9}, {'date': '2014-04-29', 'value': 81.7}, {'date': '2014-05-27', 'value': 82.2}, {'date': '2014-06-24', 'value': 86.4}, {'date': '2014-07-29', 'value': 90.3}, {'date': '2014-08-26', 'value': 93.4}, {'date': '2014-09-30', 'value': 89.0}, {'date': '2014-10-28', 'value': 94.1}, {'date': '2014-11-25', 'value': 91.0}, {'date': '2014-12-30', 'value': 93.1}, {'date': '2015-01-27', 'value': 103.8}, {'date': '2015-02-24', 'value': 98.8}, {'date': '2015-03-31', 'value': 101.4}, {'date': '2015-04-28', 'value': 94.3}, {'date': '2015-05-26', 'value': 94.6}, {'date': '2015-06-30', 'value': 99.8}, {'date': '2015-07-28', 'value': 91.0}, {'date': '2015-08-25', 'value': 101.3}, {'date': '2015-09-29', 'value': 102.6}, {'date': '2015-10-27', 'value': 99.1}, {'date': '2015-11-24', 'value': 92.6}, {'date': '2015-12-29', 'value': 96.3}, {'date': '2016-01-26', 'value': 97.8}, {'date': '2016-02-23', 'value': 94.0}, {'date': '2016-03-29', 'value': 96.1}, {'date': '2016-04-26', 'value': 94.7}, {'date': '2016-05-31', 'value': 92.4}, {'date': '2016-06-28', 'value': 97.4}, {'date': '2016-07-26', 'value': 96.7}, {'date': '2016-08-30', 'value': 101.8}, {'date': '2016-09-27', 'value': 103.5}, {'date': '2016-10-25', 'value': 100.8}, {'date': '2016-11-29', 'value': 109.4}, {'date': '2016-12-27', 'value': 113.3}, {'date': '2017-01-31', 'value': 111.6}, {'date': '2017-02-28', 'value': 116.1}, {'date': '2017-03-28', 'value': 124.9}, {'date': '2017-04-25', 'value': 119.4}, {'date': '2017-05-30', 'value': 117.6}, {'date': '2017-06-27', 'value': 117.3}, {'date': '2017-07-25', 'value': 120.0}, {'date': '2017-08-29', 'value': 120.4}, {'date': '2017-09-26', 'value': 120.6}, {'date': '2017-10-31', 'value': 126.2}, {'date': '2017-11-28', 'value': 128.6}, {'date': '2017-12-27', 'value': 123.1}, {'date': '2018-01-30', 'value': 124.3}, {'date': '2018-02-27', 'value': 130.0}, {'date': '2018-03-27', 'value': 127.0}, {'date': '2018-04-24', 'value': 125.6}, {'date': '2018-05-29', 'value': 128.8}, {'date': '2018-06-26', 'value': 127.1}, {'date': '2018-07-31', 'value': 127.9}, {'date': '2018-08-28', 'value': 134.7}, {'date': '2018-09-25', 'value': 135.3}, {'date': '2018-10-30', 'value': 137.9}, {'date': '2018-11-27', 'value': 136.4}, {'date': '2018-12-27', 'value': 126.6}, {'date': '2019-01-29', 'value': 121.7}, {'date': '2019-02-26', 'value': 131.4}, {'date': '2019-03-26', 'value': 124.1}, {'date': '2019-04-30', 'value': 129.2}, {'date': '2019-05-28', 'value': 131.3}, {'date': '2019-06-25', 'value': 124.3}, {'date': '2019-07-30', 'value': 135.8}, {'date': '2019-08-27', 'value': 134.2}, {'date': '2019-09-24', 'value': 126.3}, {'date': '2019-10-29', 'value': 126.1}, {'date': '2019-11-26', 'value': 126.8}, {'date': '2019-12-31', 'value': 128.2}, {'date': '2020-01-28', 'value': 130.4}, {'date': '2020-02-25', 'value': 132.6}, {'date': '2020-03-31', 'value': 118.8}, {'date': '2020-04-28', 'value': 85.7}, {'date': '2020-05-26', 'value': 85.9}, {'date': '2020-06-30', 'value': 98.3}, {'date': '2020-07-28', 'value': 91.7}, {'date': '2020-08-25', 'value': 86.3}, {'date': '2020-09-29', 'value': 101.3}, {'date': '2020-10-27', 'value': 101.4}, {'date': '2020-11-24', 'value': 92.9}, {'date': '2020-12-22', 'value': 87.1}, {'date': '2021-01-26', 'value': 88.9}, {'date': '2021-02-23', 'value': 90.4}, {'date': '2021-03-30', 'value': 109.0}, {'date': '2021-04-27', 'value': 117.5}, {'date': '2021-05-25', 'value': 120.0}, {'date': '2021-06-29', 'value': 128.9}, {'date': '2021-07-27', 'value': 125.1}, {'date': '2021-08-31', 'value': 115.2}, {'date': '2021-09-28', 'value': 109.8}, {'date': '2021-10-26', 'value': 111.6}, {'date': '2021-11-30', 'value': 111.9}, {'date': '2021-12-22', 'value': 115.2}, {'date': '2022-01-25', 'value': 111.1}, {'date': '2022-02-22', 'value': 105.7}, {'date': '2022-03-29', 'value': 107.6}, {'date': '2022-04-26', 'value': 108.6}, {'date': '2022-05-31', 'value': 103.2}, {'date': '2022-06-28', 'value': 98.4}, {'date': '2022-07-26', 'value': 95.3}, {'date': '2022-08-30', 'value': 103.6}, {'date': '2022-09-27', 'value': 107.8}, {'date': '2022-10-25', 'value': 102.2}, {'date': '2022-11-29', 'value': 101.4}, {'date': '2022-12-21', 'value': 109.0}, {'date': '2023-01-31', 'value': 106.0}, {'date': '2023-02-28', 'value': 103.4}, {'date': '2023-03-28', 'value': 104.0}, {'date': '2023-04-25', 'value': 103.7}, {'date': '2023-05-30', 'value': 102.5}, {'date': '2023-06-27', 'value': 110.1}, {'date': '2023-07-25', 'value': 114.0}, {'date': '2023-08-29', 'value': 108.7}, {'date': '2023-09-26', 'value': 104.3}, {'date': '2023-10-31', 'value': 99.1}, {'date': '2023-11-28', 'value': 101.0}, {'date': '2023-12-20', 'value': 108.0}, {'date': '2024-01-30', 'value': 110.9}, {'date': '2024-02-27', 'value': 104.8}, {'date': '2024-03-26', 'value': 103.1}, {'date': '2024-04-30', 'value': 97.5}]

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

def get_civiqs_sentiment_data():
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

def get_civiqs_biden_job_approval_data():
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

def get_democrat_in_white_house_data(start_date='1961-01-20'):

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

def get_frb_news_sentiment_data():
    df = pd.read_excel('https://www.frbsf.org/wp-content/uploads/sites/4/news_sentiment_data.xlsx', sheet_name='Data', names=['date', 'News Sentiment'])
    df = df.rename(columns={'News Sentiment': 'value'})
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    return df.to_dict(orient='records')

def get_gasbuddy_prices():
    gas_prices = requests.post('https://fuelinsights.gasbuddy.com/api/HighChart/GetHighChartRecords/', json={
        "regionID":[500000],
        "fuelType":3,
        "timeWindow":[13],
        "frequency":1
    }).json()
    
    return [ {'date': datetime.datetime.strptime(x['datetime'], '%m/%d/%Y').strftime('%Y-%m-%d'), 'value': x['price']} for x in gas_prices[0]['USList']]

def get_joe_biden_polling_average():
    polling_average = requests.get('https://projects.fivethirtyeight.com/polls/president-general/2024/national/polling-average.json').json()

    polling_average = [x for x in polling_average if x['candidate'] == 'Biden']

    polling_average = [ {(key if key == 'date' else 'value'): value for key, value in nested_dict.items() if key in ['date', 'pct_estimate']} for nested_dict in polling_average ]

    polling_average = sorted(polling_average, key = lambda x: x['date'])

    return polling_average

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
    
# Takes an arbitrary number of datasets and returns a list of *values* (without the dates) from those same datasets, but only for the dates for which all datasets have data points
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
    {
        'title': 'GasBuddy National Gas Prices',
        'short_title': 'GasBuddy National Gas Prices',
        'url': 'https://fuelinsights.gasbuddy.com/charts',
        'cadence': 'daily'
    },
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
    }
]

st.header("Correlation Explorer")

dataset1_picker = st.selectbox('Pick dataset #1', [x['title'] for x in eligible_datasets], index=0, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder="Choose an option", disabled=False, label_visibility="visible")
# st.caption(next((x['description'] for x in eligible_datasets if dataset1_picker == x['title'] and 'description' in x), ''))
st.caption(next((x['url'] for x in eligible_datasets if dataset1_picker == x['title']), ''))
dataset2_picker = st.selectbox('Pick dataset #2', [x['title'] for x in eligible_datasets], index=3, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder="Choose an option", disabled=False, label_visibility="visible")
# st.caption(next((x['description'] for x in eligible_datasets if dataset2_picker == x['title'] and 'description' in x), ''))
st.caption(next((x['url'] for x in eligible_datasets if dataset2_picker == x['title']), ''))

dataset_candidates = []
comparison_cadence = '%Y-%m'
for dataset_index in [1, 2]:

    if dataset_index == 1:
        dataset_value = dataset1_picker
    else:
        dataset_value = dataset2_picker

    revised_dataset = None

    # Monthly indicators
    if dataset_value == 'University of Michigan Index of Consumer Sentiment':
        dataset_candidates.append(get_umich_data(series='ics'))
    elif dataset_value == 'University of Michigan Index of Consumer Expectations':
        dataset_candidates.append(get_umich_data(series='ice'))
    elif dataset_value == 'University of Michigan Index of Current Economic Conditions':
        dataset_candidates.append(get_umich_data(series='icc'))
    elif dataset_value == 'Conference Board Consumer Confidence Index':
        dataset_candidates.append(get_conference_board_leading_indicators_data(exact_date=False))

    # Potentially daily indicators
    elif dataset_value == 'Civiqs National Economy Current Condition - Net Good':
        revised_dataset = get_civiqs_sentiment_data()
    elif dataset_value == 'A Democrat is President of the United States':
        revised_dataset = get_democrat_in_white_house_data()
    elif dataset_value == 'Federal Reserve Bank of San Francisco Daily News Sentiment Index':
        revised_dataset = get_frb_news_sentiment_data()
    elif dataset_value == 'GasBuddy National Gas Prices':
        revised_dataset = get_gasbuddy_prices()
    elif dataset_value == 'Civiqs Joe Biden Job Approval - Net Approve':
       revised_dataset = get_civiqs_biden_job_approval_data()
    elif dataset_value == '538 Joe Biden 2024 Election Polling Average':
        revised_dataset = get_joe_biden_polling_average()

    if revised_dataset is not None and next((x['cadence'] for x in eligible_datasets if x['title'] == dataset1_picker), None) == 'daily' and next((x['cadence'] for x in eligible_datasets if x['title'] == dataset2_picker), None) == 'monthly' and dataset_index == 1:
        dataset_candidates.append(average_daily_data_over_interval(revised_dataset, '%Y-%m'))
        comparison_cadence = '%Y-%m'
    elif revised_dataset is not None and next((x['cadence'] for x in eligible_datasets if x['title'] == dataset1_picker), None) == 'monthly' and next((x['cadence'] for x in eligible_datasets if x['title'] == dataset2_picker), None) == 'daily' and dataset_index == 2:
        dataset_candidates.append(average_daily_data_over_interval(revised_dataset, '%Y-%m'))
        comparison_cadence = '%Y-%m'
    elif revised_dataset is not None:
        dataset_candidates.append(revised_dataset)
        comparison_cadence = '%Y-%m-%d'

datasets = align_datasets(dataset_candidates[0], dataset_candidates[1], include_dates=True)

min_date = sorted(datasets[0], key = lambda x: x['date'])[0]['date']
max_date = sorted(datasets[0], key = lambda x: x['date'], reverse=True)[0]['date']

min_date = datetime.datetime.strptime(min_date, comparison_cadence)
max_date = datetime.datetime.strptime(max_date, comparison_cadence)


date_filter = st.slider(
    "Limit observations to a custom date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="YYYY-MM-DD"
)

datasets[0] = [x for x in datasets[0] if datetime.datetime.strptime(x['date'], comparison_cadence) >= date_filter[0] and datetime.datetime.strptime(x['date'], comparison_cadence) <= date_filter[1]]
datasets[1] = [x for x in datasets[1] if datetime.datetime.strptime(x['date'], comparison_cadence) >= date_filter[0] and datetime.datetime.strptime(x['date'], comparison_cadence) <= date_filter[1]]

if len(datasets[0]) >= 4:

    pearsons_r = calculate_pearsons([x['value'] for x in datasets[0]], [x['value'] for x in datasets[1]])

    st.metric(label="Pearson's r", value=round(pearsons_r, 3), delta="Strong" if abs(pearsons_r) >= 0.6 else "Moderate" if abs(pearsons_r) >= 0.4 else "Weak")

    st.metric(label="Observations", value=len(datasets[0]))

    dataset1_df = pd.DataFrame(datasets[0])
    dataset1_df = dataset1_df.rename(columns={"value": 'data1'})
    dataset2_df = pd.DataFrame(datasets[1])
    dataset2_df = dataset2_df.rename(columns={"value": 'data2'})

    chart_df = dataset1_df.join(dataset2_df.set_index('date'), on='date')

    if dataset1_picker != dataset2_picker:
        table_df = chart_df.rename(columns={'data1': dataset1_picker, 'data2': dataset2_picker})
        table_df = table_df[['date', dataset1_picker, dataset2_picker]]
    else:
        table_df = chart_df.rename(columns={'data1': f'1 - {dataset1_picker}', 'data2': f'2 - {dataset2_picker}'})
        table_df = table_df[['date', f'1 - {dataset1_picker}', f'2 - {dataset2_picker}']]

    dataset1_short_title = next((x['short_title'] for x in eligible_datasets if dataset1_picker == x['title']), None)
    dataset2_short_title = next((x['short_title'] for x in eligible_datasets if dataset2_picker == x['title']), None)

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
             
        The Pearson's r coefficient is a measure of the strength of correlation between two data series. (Note that Pearson's r does *not* tell us the direction of causation between the two datasets or even whether any exists at all, but simply the degree to which the two datasets are correlated.)
             
        The value of Pearson's r ranges from a minimum of -1 to a maximum of 1. A value of 1 represents perfect positive correlation while a value of -1 represents perfect negative correlation. A Pearson's r value of 0 indicates that there is no relationship whatsoever between the two datasets.
             
        In practice, no two datasets will ever be perfectly correlated or perfectly uncorrelated. Although no exact consensus exists on the threshold of 'strong' correlation, generally a Pearson's r coefficient of 0.6 or above (or -0.6 or below) is considered a strong correlation.
             
        An important detail about the Pearson's r metric is that it requires two datasets of exactly equal length. That is, a monthly dataset covering two years cannot be compared to a monthly dataset that covers only one. This presents a challenge given the variety of datasets available here.
             
        To acccount for this, I have made two key adjustments to the datasets.
             
        First, I only include the data points from *dates in common* between the two datasets being compared. For example, when comparing a monthly dataset with observations from June 2019 to May 2023 with another dataset running from August 2001 to February 2024, I will trim both datasets so they only include observations between August 2001 and May 2023, a period during which both datasets have observations.
             
        Secondly, when comparing two datasets whose observations occur at *different cadences* - e.g., one is reported monthly and the other is reported daily - I average the higher-frequency dataset over the lower-frequency cadence. An example of this would be correlating average gas prices (a dataset with daily observations) to consumer sentiment indices (which are generally measured monthly): in this case, I first average the daily gas prices for each month before correlating them with the monthly consumer sentiment index dataset.
             
        The data table directly above the line chart represents these *adjusted* datasets. (You can export/download the data to check it yourself and conduct your own analyses.) If you see any errors or bugs, please let me know!
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