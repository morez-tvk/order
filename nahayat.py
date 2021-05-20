import time
import pause
import threading
import requests
import datetime
from multiprocessing import Process
import os, signal
import datetime
from LogMg import *
import json

session = requests.session()


class NahayatNegar:
    def __init__(self, data, limit_time, servers):
        self.data_list = []
        if type(data) == list:
            for sahm in data:
                self.cookies = sahm['cookies']
                self.data_list.append(list(sahm['data'].keys())[0])
                self.headers = sahm['headers']
                self.link = sahm['url']
        elif type(data) == dict:
            self.cookies = data['cookies']
            self.data = list(data['data'].keys())[0]
            self.headers = data['headers']
            self.link = data['url']
        self.time = [int(i) for i in limit_time.split(':')]
        self.success = False
        self.time_period = 2
        self.servers = servers

    def order(self, ot):
        logger.info('sending first order')
        data = json.loads(self.data)
        data['data']['orderTicket'] = ot
        now_time = datetime.datetime.now()
        pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                       microsecond=self.time[3])
        # pause.until(pause_until)
        try:
            res = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=json.dumps(data),
                               timeout=1200000)
            ot = res.json()['customer']['orderTicket']
            data['data']['orderTicket'] = ot
        except Exception as e:
            pass
            # logger.error(res.json())
        logger.info("sending to next server")
        x = f"http://{self.servers[0]}:2020/get_next"
        print(x)
        session.post(x, json={
            "link": self.link,
            "cookies": self.cookies,
            "headers": self.headers,
            "data": json.dumps(data),
            "servers": self.servers,
            "counter": 0
        })
        try:
            logger.info(res.json())
        except Exception as e:
            pass
