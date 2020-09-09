import json

import pause

import datetime
from requests_futures.sessions import FuturesSession
from multiprocessing import Process
import threading
import time


class Ordering:
    def __init__(self, data, time):
        self.threads = []
        self.data_list = []
        if type(data) == list:
            for sahm in data:
                self.data_list.append(json.loads(list(sahm['data'].keys())[0]))
                self.headers = sahm['headers']
                self.cookies = sahm['cookies']
                self.link = sahm['url']
        elif type(data) == dict:
            self.data = json.loads(list(data['data'].keys())[0])
            self.headers = data['headers']
            self.cookies = data['cookies']
            self.link = data['url']
        self.success = False
        self.time = time
        self.buyed_quantity = 0
        self.delay = 0
        self.time_period = 10
        self.thread_local = threading.local()
        self.sem = threading.Semaphore()
        self.sem_file = threading.Semaphore()
        # self.log = open(f"log/rayan-{self.data['insMaxLcode']}--{time}--{self.data['quantity']}.json", "w")

    def multi_req(self, delay=0, time_period=5):
        print(self.data_list)
        self.delay = delay / 1000
        self.final_time = time.mktime(
            datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S").timetuple()) + time_period
        pause.until(datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        if len(self.data_list) == 0:
            t = Process(target=self.order, daemon=True)
        else:
            t = Process(target=self.sequence_order, daemon=True)
        t.start()
        wakeup_time = self.final_time - time.time()
        print(wakeup_time)
        time.sleep(wakeup_time)
        t.terminate()

    def order(self):
        print('single ordering')
        print(datetime.datetime.now())
        with FuturesSession(max_workers=1) as session:
            while True:
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, json=self.data,
                                      hooks={'response': self.response_hook}, timeout=1200000)
                if self.final_time < time.time(): break
                time.sleep(self.delay)

    def sequence_order(self):
        print('multi item ordering')
        with FuturesSession(max_workers=1) as session:
            while True:
                for sahm in self.data_list:
                    future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, json=sahm,
                                          hooks={'response': self.response_hook}, timeout=1200000)
                    if self.final_time < time.time(): break
                    time.sleep(self.delay)

    def response_hook(self, resp, *args, **kwargs):
        try:
            result = resp.json()
            print(result)
            # if result['done'] == True:
            #     self.success = True
        except:
            pass


if __name__ == '__main__':
    data = {
        "url": "https://boursebimeh.exirbroker.com/api/v1/order",
        "raw_url": "https://boursebimeh.exirbroker.com/api/v1/order",
        "method": "post",
        "cookies": {
            "PLAY_LANG": "fa",
            "cookiesession1": "65D85D98LDO1JR3LTMSGMZJ8TZCZB5BB",
            "PLAY_SESSION": "abfa8f8615e80e0df3996f7808e583b347eb327c-client_login_id=6340204e0fa04d269719bda6c0e5485c&client_id=188dc3b9cdf249ba920e6e47ceef06e9&authToken=654c60c48ef94a3fb633e3bb92cc2a0d"
        },
        "headers": {
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Content-Type": "application/json",
            "Origin": "https://boursebimeh.exirbroker.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://boursebimeh.exirbroker.com/mainNew",
            "Accept-Language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7"
        },
        "data": {
            "{\"id\":\"\",\"version\":1,\"hon\":\"\",\"bankAccountId\":-1,\"insMaxLcode\":\"IRO3KRMZ0001\",\"abbreviation\":\"\",\"latinAbbreviation\":\"\",\"side\":\"SIDE_BUY\",\"quantity\":100,\"quantityStr\":\"\",\"remainingQuantity\":0,\"price\":115939,\"priceStr\":\"\",\"tradedQuantity\":0,\"averageTradedPrice\":0,\"disclosedQuantity\":0,\"orderType\":\"ORDER_TYPE_LIMIT\",\"validityType\":\"VALIDITY_TYPE_DAY\",\"validityDate\":\"\",\"validityDateHidden\":\"hidden\",\"orderStatusId\":0,\"queueIndex\":-1,\"searchedWord\":\"\",\"coreType\":\"c\",\"marketType\":\"\",\"hasUnderCautionAgreement\":false,\"dividedOrder\":false,\"clientUUID\":\"\"}": ""
        }
    }

    pause_time = '2020-08-01 03:37:55'
    a = Ordering(data=data, time=pause_time)
    a.order()
