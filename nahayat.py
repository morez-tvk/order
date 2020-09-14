import time
import pause
from threading import Thread
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
        self.time = [int(i) for i in limit_time.split(':')]
        self.success = False
        self.time_period = 2
        # self.sem = threading.Semaphore()

    def multi_req(self, delay=0, time_period=50):
        self.delay_list = [3000]  + ([delay] * (time_period - 1))
        now_time = datetime.datetime.now()
        logger.info ("waiting to start")
        if time_period == 0:
            pause_until = now_time.replace(hour=self.time[0], minute=self.time[1], second=self.time[2],
                                           microsecond=self.time[3])
            pause.until(pause_until)
            self.infinite_order()
        else:
            pause_until = now_time.replace(hour=self.time[0], minute=self.time[1] ,second=self.time[2]-3,microsecond=self.time[3])
            print(pause_until)
            pause.until(pause_until)
            self.order()

    def order(self):
        print("here is the order function")
        with FuturesSession(max_workers=1) as session:
            print("single request")
            delay_index = 0
            while delay_index < len(self.delay_list):
                logger.info(datetime.datetime.now())
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook},timeout=1200000)
                # logger.info(delay_list [delay_index])
                # time.sleep(self.delay_list[delay_index] / 1000)
                delay_index += 1

    def infinite_order(self):
        print("here is the order function")
        with FuturesSession(max_workers=50) as session:
            print("single request")
            delay_index = 0
            while True:
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook},timeout=1200000)
                # logger.info(delay_list [delay_index])

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
            # result = resp.json()
            logger.info(resp.json())
            # logger.info(str(result))
            # if result['done'] == True:
            #     self.success = True
            #     logger.info ("done")
        except Exception as e:
            print(str(e))
            logger.info(str(e))
            pass

if __name__ == "__main__":
    ss = "09:27:45:840000"
    json = {
    "url": "https://www.nahayatnegar.com/online/order/saveOrder",
    "raw_url": "https://www.nahayatnegar.com/online/order/saveOrder",
    "method": "post",
    "cookies": {
        "__auc": "0c8e72391728da397a8b32571c2",
        "_ga": "GA1.2.640574513.1594611983",
        "_pk_id.1.97af": "845f4c6418355ef0.1591514208.3.1598508325.1594612030.",
        "_vid": "1599247594440",
        "__eid": "bbc8734b2d18b8be367d98996a0d8df6",
        "locale_dispatcher": "fa_IR",
        "ROUTEID": ".1",
        "sid": "f431e17ea0081a3c9e51fc240221ee21e04cb38ba4e0",
        "oid": "31860418b5b560bb1c732a69176b759fb38ba4e03353"
    },
    "headers": {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.nahayatnegar.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.nahayatnegar.com/online",
        "Accept-Language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7"
    },
    "data": {
        "{\"data\":{\"split\":false,\"edit\":false,\"price_percent\":[1740,1758,1776,1794,1812,1830,1848,1866,1884,1902,1920],\"minPrice\":1740,\"maxPrice\":1920,\"minLot\":1,\"maxLot\":400000,\"volume_steps\":[40000,80000,120000,160000,200000,240000,280000,320000,360000,400000],\"csrf\":\"c71f13dfc41aa6bda2f03285d098e94f\",\"inst\":\"IRO1TOOM0001\",\"paymentType\":\"2\",\"limitType\":\"1\",\"dueType\":\"1\",\"bondInterest\":null,\"deduct\":{\"cr\":\"0.003040000000\",\"xc\":\"300000000\",\"tx\":\"0.000000000000\",\"bcr\":\"0.000256000000\",\"xbcr\":\"300000000\",\"fcr\":\"0.000000000000\",\"xfcr\":\"99999999999\",\"scr\":\"0.000240000000\",\"xscr\":\"100000000\",\"ccr\":\"0.000080000000\",\"xccr\":\"134000000\",\"tcr\":\"0.000080000000\",\"xtcr\":\"80000000\",\"rbcr\":\"0.000016000000\",\"xrbcr\":\"26000000\"},\"calcShow\":false,\"showCalc\":false,\"grandTotal\":770850816,\"price\":1920,\"volume\":400000,\"draft\":false,\"diffVolume\":400000,\"orderForm\":\"buy\",\"displayVolume\":0}}": ""
    }

}
    a = NahayatNegar(limit_time=ss , data= json)
    a.multi_req()