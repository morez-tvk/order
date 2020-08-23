import json

import pause

import datetime

import concurrent.futures
import requests
import threading
import time


class Ordering:
    def __init__(self, data, time):
        self.threads = []
        self.data = json.loads(list(data['data'].keys())[0])
        self.headers = data['headers']
        self.cookies = data['cookies']
        self.link = data['url']
        self.success = False
        self.time = time
        self.buyed_quantity = 0
        self.delay = 0
        self.time_period = 2
        self.thread_local = threading.local()
        self.sem = threading.Semaphore()
        self.sem_file = threading.Semaphore()
        self.log = open(f"log/rayan-{self.data['insMaxLcode']}--{time}--{self.data['quantity']}.json", "w")

    def multi_req(self, delay=0, time_period=15):
        self.delay = delay
        self.time_period = time_period
        pause.until(datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as self.executor:
            print('creating a thread')
            self.futures = [self.executor.submit(self.order) for _ in range(500)]

    def cancel_order(self):
        try:
            self.executor.shutdown(wait=False)
        except:
            print("ERROR on Canceling thread")

    def get_session(self):
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session

    def order(self):
        # print('new thread')

        session = self.get_session()
        print(self.data)
        while time.time() < time.mktime(
                datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S").timetuple()) + self.time_period:
            with session.post(url=self.link, json=self.data, headers=self.headers, cookies=self.cookies,
                              timeout=100) as response:
                pass
                # print(response.json())
        print('finished')

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
