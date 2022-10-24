import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {'User-Agent': "Chrome/54.0.2840.90"}
tickers = ["AAPL", "META", "TSLA", "GOOGL"]
df = pd.DataFrame()
for ticker in tickers:
    url = ("http://finviz.com/quote.ashx?t=" + ticker.lower())
    response = requests.get(url, headers=headers)
    html = response.content
    fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]
    cols = []
    for i in range(fundamentals.shape[1]):
        if i % 2 == 0: 
            cols.append(fundamentals.loc[:,i:i+1])
    arr = np.array(cols)
    res = pd.DataFrame(arr.reshape(int(((fundamentals.shape[0])**2)/2),2), columns = ['Measure', 'Value'])
    df = pd.concat([df, res])
df['Ticker'] = np.array([np.repeat(ticker, int((fundamentals.shape[0])**2/2)) for ticker in tickers]).reshape(int((fundamentals.shape[0])**2/2)*len(tickers),1)
df.set_index('Ticker', inplace= True)

df.head(50)