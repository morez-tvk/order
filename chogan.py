import time
import pause
import requests
from threading import Thread
import datetime, json
from requests_futures.sessions import FuturesSession
from multiprocessing import Process

class Chogan:
    def __init__(self, data, limit_time):
        self.data = data
        # self.cookies = data['headers']
        self.data = json.loads(list(data['data'].keys())[0])
        self.time = limit_time
        # self.sem = threading.Semaphore()
        # self.sem_file = threading.Semaphore()
        self.log = open(f"log/chogan-{self.data['InstrumentCode']}--{time.time()}", "w")
        self.link = data['url']
        self.success = False
        self.headers = data['headers']
        self.session = FuturesSession()

    def multi_req(self, delay=0, time_period=None):
        final_time = time.mktime(
            datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S").timetuple()) + time_period
        pause.until(datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        # start = time.time()
        t = Thread(target=self.order)
        t.start()
        while True:
            if time.time() > final_time:
                t.terminate()
                t.join(0)
                break

    def order(self):
        with FuturesSession(max_workers=500) as session:
            while True:
                future = session.post(url=self.link, headers=self.headers, json=self.data,
                                      hooks={'response': self.response_hook})

    def response_hook(self, resp, *args, **kwargs):
        # parse the json storing the result on the response object
        self.sem.acquire()
        json.dump(resp.json(), self.log, ensure_ascii=False, indent=4)
        self.sem.release()
