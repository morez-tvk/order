import time
import pause
from requests_futures.sessions import FuturesSession
import datetime
import json
from LogMg import *

class OnlinePlus:
    def __init__(self, data, limit_time):
        self.data_list = []
        if type(data) == list:
            for sahm in data:
                self.data_list.append(json.loads(list(sahm['data'].keys())[0]))
                self.headers = sahm['headers']
                self.link = sahm['url']
        elif type(data) == dict:
            self.data = json.loads(list(data['data'].keys())[0])
            self.headers = data['headers']
            self.link = data['url']
        self.time = [int(i) for i in limit_time.split(':')]
        self.success = False

    def multi_req(self, delay=0, count=50 , workers=1 , finish_time=None):
        self.delay = delay
        self.count = count
        self.workers = workers
        logger.info("waiting to start")
        now_time = datetime.datetime.now()
        if finish_time is not None:
            self.finish_time = [int(i) for i in finish_time.split(':')]
            self.finish_time = now_time.replace(hour=self.finish_time[0], minute=self.finish_time[1], second=self.finish_time[2],
                             microsecond=self.finish_time[3])
            if len(self.data_list) == 0:
                self.order_by_time()
            else:
                self.sequence_order_by_time()
            return
        if count == 0:
            pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                           microsecond=self.time[3])
            pause.until(pause_until)
            self.infinite_order()
        else:
            if len(self.data_list) == 0:
                self.order_by_count()
            else:
                self.sequence_order()

    def order_by_time(self):
        now_time = datetime.datetime.now()
        pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                       microsecond=self.time[3])
        pause.until(pause_until)
        with FuturesSession(max_workers=self.workers) as session:
            print("single request")
            while True:
                logger.info(datetime.datetime.now())
                future = session.post(url=self.link, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook},timeout=1200000)
                if datetime.datetime.now() > self.finish_time:
                    break

    def sequence_order_by_time(self):
        now_time = datetime.datetime.now()
        pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                       microsecond=self.time[3])
        pause.until(pause_until)
        with FuturesSession(max_workers=self.workers) as session:
            print("single request")
            while True:
                logger.info(datetime.datetime.now())
                for sahm in self.data_list:
                    future = session.post(url=self.link, headers=self.headers, data=sahm,
                                          hooks={'response': self.response_hook},timeout=1200000)
                    if datetime.datetime.now() > self.finish_time:
                        break

    def order_by_count(self):
        print("single request")

        now_time = datetime.datetime.now()
        pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                       microsecond=self.time[3])
        pause.until(pause_until)
        with FuturesSession(max_workers=self.workers) as session:
            delay_index = 0
            for i in range(self.count):
                logger.info(datetime.datetime.now())
                future = session.post(url=self.link, headers=self.headers, json=self.data,
                                      hooks={'response': self.response_hook},timeout=1200000)
                # time.sleep(self.delay)


    def infinite_order(self):
        print("here is the order function")
        with FuturesSession(max_workers=self.workers) as session:
            print("single request")
            delay_index = 0
            while True:
                future = session.post(url=self.link, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook},timeout=1200000)
                # logger.info(delay_list [delay_index])

    def sequence_order(self):
        print('multi item ordering')
        now_time = datetime.datetime.now()
        pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                       microsecond=self.time[3])
        pause.until(pause_until)
        with FuturesSession(max_workers=self.workers) as session:
            i = 0
            while i < self.count:
                for sahm in self.data_list:
                    logger.info(datetime.datetime.now())
                    future = session.post(url=self.link, headers=self.headers, data=sahm,
                                          hooks={'response': self.response_hook}, timeout=1200000)
                    i += 1
                    # time.sleep(self.delay)

    def response_hook(self, resp, *args, **kwargs):
        try:
            logger.info(resp.json())
        except Exception as e:
            print(str(e))
            logger.info(str(e))
            pass
