import time
import pause
import requests
import threading
import datetime, json



class TadbirOrder:
    def __init__(self, data , time):
        self.data = data
        self.cookies = data['cookies']
        self.data = list(data['data'].keys())[0]
        self.time = time
        self.sem = threading.Semaphore()
        self.sem_file = threading.Semaphore()
        self.log = open(f"log/Tadbir-{self.data['isin']}--{time}--{self.data['orderCount']}.json", "w")
        self.link = data['url']
        self.success = False
        self.headers = data['headers']

    def order(self):

        try:
            result = requests.post(self.link, cookies=self.cookies,
                                   headers=self.headers, json=self.data)
            print(result.json())
            result = dict(result.json())
            result['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.sem_file.acquire()
            json.dump(result, self.log, ensure_ascii=False, indent=4)
            self.sem_file.release()
        except Exception as e:
            print(e)

        try:
            self.sem.acquire()
            if result['IsSuccessfull']:
                self.success = True
            self.sem.release()
        except:
            pass

    def multi_req(self, delay=0, time_period=None):
        pause.until(datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S"))
        self.threads = []
        while True:
            self.sem.acquire()
            if time_period != None:
                if time.time() > time.mktime(
                        datetime.datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S").timetuple()) + time_period:
                    self.cancel_order()
                    return

            elif not self.success:
                self.sem.release()
                self.threads.append(threading.Thread(target=self.order))
                self.threads[-1].start()
                time.sleep(delay)
            else:
                self.sem.release()
                self.cancel_order()
                return

    def cancel_order(self):
        for i in self.threads:
            i.join(0)