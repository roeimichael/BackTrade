import requests
import pandas as pd
import csv
from datetime import datetime


def get_stock_table(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    ticker_series = pd.read_html(r.text)
    return ticker_series


def api_manage(flt, pageNbr):
    url = f"https://apewisdom.io/api/v1.0/filter/{flt}/page/{pageNbr}"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    return r


if __name__ == '__main__':
    # url = r"https://apewisdom.io/"
    flt = "all-stocks"
    pageNbr = "1"
    table = api_manage(flt, pageNbr)
    x = table.json()
    df = pd.DataFrame(x['results'])
    df = df.drop(columns=['name', 'rank_24h_ago', 'mentions_24h_ago'])
    row = df['ticker'].astype(str) + "-" + df["mentions"]
    date = datetime.today().strftime('%Y-%m-%d')
    row = row.tolist()
    row.insert(0, date)
    with open(r'ape_wisdom.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)
