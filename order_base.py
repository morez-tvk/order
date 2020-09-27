import time
import pause
from requests_futures.sessions import FuturesSession
import datetime
from LogMg import *

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
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
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
                    future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=sahm,
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
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook},timeout=1200000)
                # time.sleep(self.delay)


    def infinite_order(self):
        print("here is the order function")
        with FuturesSession(max_workers=self.workers) as session:
            print("single request")
            delay_index = 0
            while True:
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
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
                    future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=sahm,
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