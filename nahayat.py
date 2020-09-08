import time
import pause
import threading
import datetime
from requests_futures.sessions import FuturesSession
from multiprocessing import Process
import os, signal
import datetime

delay_list = [1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
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
10,
12,
15,
18,
22,
25,
25,
30,
30,
30,
30,
35,
35,
35,
40,
40,
40,
50,
50,
50,
50,
100,
200,
300,
500,
1000,
2000]


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
        self.time = limit_time
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
        t = Process(target=self.order, daemon=True)
        print ("t created")
        pause_until = now_time.replace(hour=8, minute=29,second=59,microsecond=990000)
        pause.until(pause_until)
        t.start()
        wakeup_time = 2000
        time.sleep(wakeup_time)
        t.terminate()

    def order(self):
        print('single ordering')
        print(datetime.datetime.now())
        with FuturesSession(max_workers=1) as session:
            delay_index = 0
            while not self.success:
                future = session.post(url=self.link, cookies=self.cookies, headers=self.headers, data=self.data,
                                      hooks={'response': self.response_hook}, timeout=1200000)
                if delay_index >= len(delay_list):
                    print ("failed")
                    break
                print(delay_list [delay_index])
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
            print(result)
            if result['done'] == True:
                self.success = True
                print ("done")
        except:
            pass


if __name__ == '__main__':
    data = {
    "url": "https://www.nahayatnegar.com/online/order/saveOrder",
    "raw_url": "https://www.nahayatnegar.com/online/order/saveOrder",
    "method": "post",
    "cookies": {
        "_vid": "1598986782105",
        "_pk_id.1.97af": "a4caaaea7583eccc.1598986787.8.1599599274.1599451294.",
        "__auc": "24768a491744b0a1c608207f36e",
        "_ga": "GA1.2.1463733646.1598986789",
        "__eid": "e60cb2387b1eea34ef2539baea34820f",
        "locale_dispatcher": "fa_IR",
        "ROUTEID": ".1",
        "__asc": "da2dff221746f8bc2c47d4b8ece",
        "_pk_ses.1.97af": "1",
        "_gid": "GA1.2.1330500911.1599599265",
        "_gat_gtag_UA_56428553_2": "1",
        "oid": "31860418b5b560bb1c732a69176b759fe1fdf72f8939",
        "sid": "f431e17ea0081a3c9e51fc240221ee21fdf72f893924"
    },
    "headers": {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://www.nahayatnegar.com",
        "Connection": "keep-alive",
        "Referer": "https://www.nahayatnegar.com/online"
    },
    "data": {
        "{\"data\":{\"split\":false,\"edit\":false,\"price_percent\":[15300,15460,15620,15780,15940,16100,16260,16420,16580,16740,16900],\"minPrice\":15300,\"maxPrice\":16900,\"minLot\":1,\"maxLot\":100000,\"volume_steps\":[10000,20000,30000,40000,50000,60000,70000,80000,90000,100000],\"csrf\":\"ad4e377ce4ae0adba87fb456407a44e5\",\"inst\":\"IRO1TSAN0001\",\"paymentType\":\"2\",\"limitType\":\"1\",\"dueType\":\"1\",\"bondInterest\":null,\"deduct\":{\"cr\":\"0.003040000000\",\"xc\":\"300000000\",\"tx\":\"0.000000000000\",\"bcr\":\"0.000256000000\",\"xbcr\":\"300000000\",\"fcr\":\"0.000000000000\",\"xfcr\":\"99999999999\",\"scr\":\"0.000240000000\",\"xscr\":\"100000000\",\"ccr\":\"0.000080000000\",\"xccr\":\"134000000\",\"tcr\":\"0.000080000000\",\"xtcr\":\"80000000\",\"rbcr\":\"0.000016000000\",\"xrbcr\":\"26000000\"},\"calcShow\":false,\"showCalc\":false,\"grandTotal\":15356792,\"price\":\"15300\",\"volume\":\"1000\",\"draft\":false,\"diffVolume\":\"1000\",\"orderForm\":\"buy\",\"displayVolume\":0}}": ""
    }
}





    #
    pause_time = '2020-09-09 01:55:05'
    a = NahayatNegar(data=data, limit_time=pause_time)
    print(a.multi_req(delay=300, time_period=100))
