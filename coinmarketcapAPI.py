import os
import requests
import pandas as pd
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
from time import sleep
from time import time



load_dotenv()

api_key = os.getenv("cmc_key")
base_url = "https://pro-api.coinmarketcap.com"
listings_url = '/v1/cryptocurrency/listings/latest'
all_data = pd.DataFrame()

# Set parameters
parameters = {
    'start':'1',
    'limit':'15',
    'convert':'USD'
}

# Set Headers
headers = {
    'X-CMC_PRO_API_KEY': api_key,
    'Accepts': 'application/json'
}

def get_cmc_data(endpoint,params=None):
    if params == None:
            params = {}
    
    endpoint_url = base_url + endpoint
    
    try:
        response = requests.get(endpoint_url,
                                params=params,
                                headers=headers)
        print('requesting'+response.url)
        
        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print(f'Error:{response.status_code}')
            return
        
    except Exception as e:
        print(f'An error occurred:{e}')
    

for i in range(36):
    listings_data = get_cmc_data(listings_url,params=parameters)
    listings_df = pd.DataFrame(listings_data['data'])
    listings_data = pd.concat([
        listings_df,
        listings_df.quote.apply(pd.Series).USD.apply(pd.Series)],
        axis=1)
    listings_data_df = listings_data.drop('quote',axis=1)
    all_data = pd.concat([all_data, listings_data_df], ignore_index=True)
    print(f'Batch {i+1} extracted')
    sleep(300)

all_data.to_csv('historical_data.csv', index=False)


