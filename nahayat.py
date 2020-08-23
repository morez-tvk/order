import time
import pause
import threading
import datetime, json,requests
from requests_futures.sessions import FuturesSession
from multiprocessing import Process


class NahayatNegar:
    def __init__(self, data, limit_time):
        self.cookies = data['cookies']
        self.time = limit_time
        self.success = False
        self.time_period = 2
        self.sem = threading.Semaphore()
        self.data = list(data['data'].keys())[0]
        # self.data = json.loads(self.data)
        print(self.data)
        # self.log = open(f"log/{self.data['data']['inst']}--{time.time()}.json", "w")
        self.headers = data['headers']
        self.link = data['url']

    def multi_req(self, delay=0, time_period=5):
        final_time = time.mktime(
            datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S").timetuple()) + time_period
        pause.until(datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        # start = time.time()
        t = Process(target=self.order, daemon=True)
        t.start()
        while True:
            if time.time() > final_time:
                t.terminate()
                t.join(0)
                break

    def order(self):
        print(self.link,self.cookies,self.headers,self.data)
        with FuturesSession(max_workers=500) as session:
            while True:
                future = session.post(url=self.link,cookies=self.cookies, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook}, timeout=1200000)

    def response_hook(self, resp, *args, **kwargs):
        # parse the json storing the result on the response object
        print(resp.json())
        # json.dump(resp.json(), self.log, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data = {
    "url": "https://www.nahayatnegar.com/online/order/saveOrder",
    "raw_url": "https://www.nahayatnegar.com/online/order/saveOrder",
    "method": "post",
    "cookies": {
        "_vid": "1589271606842",
        "__auc": "0c8e72391728da397a8b32571c2",
        "_ga": "GA1.2.640574513.1594611983",
        "_pk_id.1.97af": "845f4c6418355ef0.1591514208.2.1594612030.1594611982.",
        "__eid": "73ba7f00447a96ec58a8009a63975d4b",
        "locale_dispatcher": "fa_IR",
        "ROUTEID": ".1",
        "sid": "f431e17ea0081a3c9e51fc240221ee21f5a80f20ac56",
        "oid": "31860418b5b560bb1c732a69176b759ffb71dd7f5a80"
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
        "{\"data\":{\"split\":false,\"edit\":false,\"price_percent\":[22370,22604,22838,23072,23306,23540,23774,24008,24242,24476,24710],\"minPrice\":22370,\"maxPrice\":24710,\"minLot\":1,\"maxLot\":100000,\"volume_steps\":[10000,20000,30000,40000,50000,60000,70000,80000,90000,100000],\"csrf\":\"e310f515b1066ae85c254296776b84f7\",\"inst\":\"IRO1SITA0001\",\"paymentType\":\"2\",\"limitType\":\"1\",\"dueType\":\"1\",\"bondInterest\":null,\"deduct\":{\"cr\":\"0.003040000000\",\"xc\":\"300000000\",\"tx\":\"0.000000000000\",\"bcr\":\"0.000256000000\",\"xbcr\":\"300000000\",\"fcr\":\"0.000000000000\",\"xfcr\":\"99999999999\",\"scr\":\"0.000240000000\",\"xscr\":\"100000000\",\"ccr\":\"0.000080000000\",\"xccr\":\"134000000\",\"tcr\":\"0.000080000000\",\"xtcr\":\"80000000\",\"rbcr\":\"0.000016000000\",\"xrbcr\":\"26000000\"},\"calcShow\":false,\"showCalc\":false,\"grandTotal\":1166177038,\"price\":24710,\"calcValue\":0,\"volume\":47020,\"draft\":false,\"diffVolume\":47020,\"orderForm\":\"buy\",\"displayVolume\":0}}": ""
    }
}


    pause_time = '2020-08-10 07:54:25'
    a = NahayatNegar(data=data, limit_time=pause_time)
    print(a.multi_req())
