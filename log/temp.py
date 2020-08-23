import requests

headers = {
    'authority': 'rlcwebapi.tadbirrlc.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://silver.mobinsb.com',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://silver.mobinsb.com/Contents/Default/Modules/TradingView/TadbirTVChart/index.html?currentTheme=default&UserName=msb01315031&isin=&version=3.6.1.50664',
    'accept-language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
}

params = (
    ('symbol', 'IRO1MKBT0001_1'),
    ('resolution', 'D'),
    ('from', '1597327780'),
    ('to', '1598191780'),
)

response = requests.get('https://rlcwebapi.tadbirrlc.com/ChartData/history', headers=headers, params=params)
print(response.json())
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://rlcwebapi.tadbirrlc.com/ChartData/history?symbol=IRO1MKBT0001_1&resolution=D&from=1597327780&to=1598191780', headers=headers)
