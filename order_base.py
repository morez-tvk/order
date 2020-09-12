
import time
import pause
import threading
import datetime
from requests_futures.sessions import FuturesSession
from multiprocessing import Process
import os, signal
import datetime
from LogMg import *


delay_list = \
    [5,
5,
5,
5,
5,
5,
5,
5,
5,
3,
2,
2,
2,
2,
2,
2,
2,
2,
2,
2,
2,
2,
2,
2,
2,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
5,
10,
25,
50,
50,
100,
100,
200,
300]


class Order:
    def __init__(self, data, limit_time):
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
        self.time = limit_time.split(':')
        self.success = False
        self.time_period = 2

    def multi_req(self, delay=0, time_period=5):
        print(self.data_list)
        now_time = datetime.datetime.now()
        logger.info(now_time)
        logger.info ("t created")
        if len(self.data_list) == 0:
            pause_until = now_time.replace(hour=20, minute=delay,second=29,microsecond=900000)
            pause.until(pause_until)
            self.order()
        else:
            pause_until = now_time.replace(hour=20, minute=delay, second=29, microsecond=900000)
            pause.until(pause_until)
            self.sequence_order()

    def order(self):
        logger.info('single ordering')
        with FuturesSession(max_workers=1) as session:
            delay_index = 0
            while delay_index < len(delay_list):
                logger.info(datetime.datetime.now())
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook}, timeout=1200000)
                logger.info(delay_list [delay_index])
                time.sleep(delay_list [delay_index]/1000)
                delay_index += 1

    def sequence_order(self):
        print('multi item ordering')
        with FuturesSession(max_workers=1) as session:
            while True:
                for sahm in self.data_list:
                    future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=sahm,
                                          hooks={'response': self.response_hook}, timeout=1200000)

    def response_hook(self, resp, *args, **kwargs):
        try:
            result = resp.json()
            logger.info(str(result))
        except Exception as e:
            logger.info(str(e))
            pass