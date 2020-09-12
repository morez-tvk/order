import time
import pause
import threading
import datetime
from requests_futures.sessions import FuturesSession
from multiprocessing import Process
import os, signal
import datetime
from LogMg import *


delay_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


class NahayatNegar:
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
        self.sem = threading.Semaphore()

    def multi_req(self, delay=0, time_period=5):
        print(self.data_list)
        #self.delay = delay / 1000
        # final_time = time.mktime(
        #     datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S").timetuple()) + time_period
        #pause.until(datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        now_time = datetime.datetime.now()
        logger.info(now_time)
        t = Process(target=self.order, daemon=True)
        logger.info ("t created")
        print("pausing")
        pause_until = now_time.replace(hour=9, minute=37 ,second=20,microsecond=980000)
        print(pause_until)
        pause.until(pause_until)
        print("begin")
        #self.order()
        t.start()
        #wakeup_time = 2000
        #time.sleep(wakeup_time)
        #t.terminate()

    def order(self):
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
            delay_index = 0
            while delay_index < len(delay_list):
                for sahm in self.data_list:
                    future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=sahm,
                                          hooks={'response': self.response_hook}, timeout=1200000)
                    time.sleep(delay_list[delay_index] / 1000)
                    delay_index += 1

    def response_hook(self, resp, *args, **kwargs):
        try:
            result = resp.json()
            print(result)
            logger.info(str(result))
            # if result['done'] == True:
            #     self.success = True
            #     logger.info ("done")
        except Exception as e:
            logger.info(str(e))
            pass
