import requests

cookies = {
    '_ga': 'GA1.2.920591275.1599661713',
    '_gid': 'GA1.2.1699366324.1599661713',
    '.ASPXAUTH': '833F8864A4A0FC688A688824907971A05F1BFDC2A0FD03A8FB90645420F8A868A85D44E8CAABD0A4D3B8B3B701362F42975CA8B61597265AD3A842CC3559B82FECF2A3A40DAEDB0F17BC96A06775CE52DFFBAE158E1EEBE907A7BB4F020BD71CE88CE887503BDF24DA191BF66A2963AE405FAC24E262FEADD73647C2C03AFC27C5135B732CBBE6D6663228345F810279E096D908463B9266A5DB621AF43F909314F2D189EDFCA43CAD34ABD2226182CE3E9724DD08E8FA3C29FE6D6367D0BD32D3A6C542F27DFE05ED186B99F3A5CBF9C797C54006556E8AA5807E0D48B65360',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'text/plain, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://online.kian.trade',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://online.kian.trade/',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = (
    ('transport', 'longPolling'),
    ('connectionToken', '3hEIYY8JQpHcK39kuJ/KAMEEAokLN8ZHVp6hVI0619HsjegoDKN2/Hv9LFwwDNFC9Wli0y55lCVpbLVGQhdfRpbCrtOTIx6LMBShT2AVIseo6X3bWWnuWbtgVCDlnXEu'),
    ('s_id', '529466'),
    ('connectionData', '[{"name":"accounttradehub"},{"name":"assetstatehub"},{"name":"balancehub"},{"name":"bidaskfirstorderhub"},{"name":"bidaskhub"},{"name":"charthub"},{"name":"clubscorehub"},{"name":"exchangestatehub"},{"name":"feedhub"},{"name":"indexhub"},{"name":"instrumentgroupstatehub"},{"name":"instrumentsummaryhub"},{"name":"intradaytradehub"},{"name":"messagehub"},{"name":"orderhub"},{"name":"portfoliohub"},{"name":"reporthub"},{"name":"timehub"},{"name":"tradehub"},{"name":"tradesummaryhub"},{"name":"transactionhub"},{"name":"ytmhub"}]'),
)

data = {
  'data': '{"H":"onlinetradinghub","M":"NewOrder","A":["13093","1","0","15248","1",null,"1","16210","338",null,"35b6cf91-5baf-49c6-c995-a8e04c3e179a",100000,null,"",false,null,"",false],"I":88}'
}

response = requests.post('https://hub.online.kian.trade/signalr/send', headers=headers, params=params, cookies=cookies, data=data, verify=False)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://hub.online.kian.trade/signalr/send?transport=longPolling&connectionToken=3hEIYY8JQpHcK39kuJ%2FKAMEEAokLN8ZHVp6hVI0619HsjegoDKN2%2FHv9LFwwDNFC9Wli0y55lCVpbLVGQhdfRpbCrtOTIx6LMBShT2AVIseo6X3bWWnuWbtgVCDlnXEu&s_id=529466&connectionData=%5B%7B%22name%22%3A%22accounttradehub%22%7D%2C%7B%22name%22%3A%22assetstatehub%22%7D%2C%7B%22name%22%3A%22balancehub%22%7D%2C%7B%22name%22%3A%22bidaskfirstorderhub%22%7D%2C%7B%22name%22%3A%22bidaskhub%22%7D%2C%7B%22name%22%3A%22charthub%22%7D%2C%7B%22name%22%3A%22clubscorehub%22%7D%2C%7B%22name%22%3A%22exchangestatehub%22%7D%2C%7B%22name%22%3A%22feedhub%22%7D%2C%7B%22name%22%3A%22indexhub%22%7D%2C%7B%22name%22%3A%22instrumentgroupstatehub%22%7D%2C%7B%22name%22%3A%22instrumentsummaryhub%22%7D%2C%7B%22name%22%3A%22intradaytradehub%22%7D%2C%7B%22name%22%3A%22messagehub%22%7D%2C%7B%22name%22%3A%22orderhub%22%7D%2C%7B%22name%22%3A%22portfoliohub%22%7D%2C%7B%22name%22%3A%22reporthub%22%7D%2C%7B%22name%22%3A%22timehub%22%7D%2C%7B%22name%22%3A%22tradehub%22%7D%2C%7B%22name%22%3A%22tradesummaryhub%22%7D%2C%7B%22name%22%3A%22transactionhub%22%7D%2C%7B%22name%22%3A%22ytmhub%22%7D%5D', headers=headers, cookies=cookies, data=data, verify=False)
