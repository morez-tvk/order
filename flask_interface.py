from flask_restful import Resource, request
from nahayat import NahayatNegar
from rayan import Ordering
from tadbir import TadbirOrder
from chogan import Chogan
from datax import Datax
import flask
from multiprocessing import Process

import threading
from threading import Thread
import json


def input_validator(request):
    try:
        text_json = request.data
        jsonObj = json.loads(text_json)
    except:
        return False
    return True


# https://www.nahayatnegar.com/online/order/saveOrder

rayan_oid = 0
rayan_orders = {}
rayan_l_o = {}


class set_order(Resource):
    print("starting")

    def post(self):
        global rayan_oid
        global rayan_orders
        global rayan_l_o
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = dict(json.loads(text_json))
        if data['status'] == 'set':
            rayan_oid += 1
            time_period = data.get('time_period', None)
            delay = data.get('delay', 0)
            rayan_orders[rayan_oid] = Ordering(data=data['json'],
                                               time=data['time'])
            t = Process(target=rayan_orders[rayan_oid].multi_req, args=(delay, time_period))
            t.start()
            rayan_l_o[rayan_oid] = t
            # self.orders[self.rayan_oid["id"]].multi_req(delay=data['delay'])
            return {'id': rayan_oid, 'status': 200}

        elif data['status'] == 'cancel':
            try:
                # rayan_orders[data['id']].cancel_order()
                rayan_l_o[data['id']].terminate()
                rayan_l_o[data['id']].join(0)
                rayan_orders.pop(data['id'])
                return {"message": f"order {data['id']} deleted from queue"}
            except:
                flask.abort(500, "No such order in queue")


oid = 0
orders = {}
l_o = {}


class nahayat_negar(Resource):

    def post(self):
        global oid
        global l_o
        global orders
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = json.loads(text_json)
        if data['status'] == 'set':
            oid += 1
            time_period = data.get('time_period', 20)
            delay = data.get('delay', 0)
            orders[oid] = NahayatNegar(data=data['json'], limit_time=data['time'])
            t = Thread(target=orders[oid].multi_req, args=(delay, time_period))
            t.start()
            print ("wating ...")
            # orders [oid].multi_req (delay, time_period)
            #l_o[oid] = t
            return {'id': oid, 'status': 200}

        elif data['status'] == 'cancel':
            try:
                l_o[data['id']].terminate()
                l_o[data['id']].join(0)
                orders.pop(data['id'])
                return {"message": f"order {data['id']} deleted from queue"}
            except:
                flask.abort(500, "No such order in queue")

tadbir_oid = 0
tadbir_l_o = {}
tadbir_orders = {}
class Tadbir(Resource):

    def post(self):
        global tadbir_oid
        global tadbir_l_o
        global tadbir_orders
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = json.loads(text_json)
        if data['status'] == 'set':
            tadbir_oid += 1
            time_period = data.get('time_period', None)
            tadbir_orders[tadbir_oid] = TadbirOrder(time=data['time'] , data=data['json'])
            t = threading.Thread(target=tadbir_orders[tadbir_oid].multi_req, args=(data['delay'], time_period), daemon=True)
            t.start()
            tadbir_l_o[tadbir_oid] = t
            # tadbir_orders[self.tadbir_oid["id"]].multi_req(delay=data['delay'])
            return {'id': tadbir_oid, 'status': 200}

        elif data['status'] == 'cancel':
            try:
                tadbir_l_o[data['id']].join(0)
                tadbir_orders.pop(data['id'])
                return {"message": f"order {data['id']} deleted from queue"}
            except:
                flask.abort(500, "No such order in queue")


chogan_oid = 0
chogan_orders = {}
chogan_o = {}


class chogan(Resource):

    def post(self):
        global chogan_oid
        global chogan_o
        global chogan_orders
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = json.loads(text_json)
        if data['status'] == 'set':
            chogan_oid += 1
            time_period = data.get('time_period', 20)
            delay = data.get('delay', 0)
            chogan_orders[chogan_oid] = Chogan(data=data['json'], limit_time=data['time'])
            t = Process(target=chogan_orders[chogan_oid].multi_req, args=(delay, time_period))
            t.start()
            chogan_o[chogan_oid] = t
            # chogan_orders[self.chogan_oid["id"]].multi_req(delay=data['delay'])
            return {'id': chogan_oid, 'status': 200}

        elif data['status'] == 'cancel':
            try:
                chogan_o[data['id']].terminate()
                chogan_o[data['id']].join(0)
                chogan_orders.pop(data['id'])
                return {"message": f"order {data['id']} deleted from queue"}
            except:
                flask.abort(500, "No such order in queue")

datax_oms_oid = 0
datax_oms_orders = {}
datax_oms_o = {}


class datax_oms(Resource):

    def post(self):
        print('post')
        global datax_oms_oid
        global datax_oms_o
        global datax_oms_orders
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = json.loads(text_json)
        if data['status'] == 'set':
            datax_oms_oid += 1
            time_period = data.get('time_period', 20)
            delay = data.get('delay', 0)
            datax_oms_orders[datax_oms_oid] = Datax(data=data['json'], limit_time=data['time'])
            t = Process(target=datax_oms_orders[datax_oms_oid].multi_req, args=(delay, time_period))
            t.start()
            datax_oms_o[datax_oms_oid] = t
            # datax_oms_orders[self.datax_oms_oid["id"]].multi_req(delay=data['delay'])
            return {'id': datax_oms_oid, 'status': 200}

        elif data['status'] == 'cancel':
            try:
                datax_oms_o[data['id']].terminate()
                datax_oms_o[data['id']].join(0)
                datax_oms_orders.pop(data['id'])
                return {"message": f"order {data['id']} deleted from queue"}
            except:
                flask.abort(500, "No such order in queue")