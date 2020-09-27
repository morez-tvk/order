from flask_restful import Resource, request
from nahayat import NahayatNegar
from order_base import Order
from tadbir import OnlinePlus
import flask
from multiprocessing import Process
import json

def input_validator(request):
    try:
        text_json = request.data
        jsonObj = json.loads(text_json)
    except:
        return False
    return True


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
            t = Process(target=orders[oid].multi_req, args=(delay, time_period))
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

class Ordering(Resource):
    def post(self):
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = json.loads(text_json)
        count = data.get('count', 20)
        finish_time = data.get('finish_time', None)
        workers = data.get('workers', 1)
        delay = data.get('delay', 0)
        order =  Order(data=data['json'], limit_time=data['time'])
        order.multi_req(count=count, delay=delay , finish_time = finish_time , workers = workers)
        return {'status': 200}

class Tadbir(Resource):
    def post(self):
        if input_validator(request) == False:
            flask.abort(400, "The input should be json.")
        text_json = request.data
        data = json.loads(text_json)
        count = data.get('count', 20)
        finish_time = data.get('finish_time', None)
        workers = data.get('workers', 1)
        delay = data.get('delay', 0)
        order =  OnlinePlus(data=data['json'], limit_time=data['time'])
        order.multi_req(count=count, delay=delay , finish_time = finish_time , workers = workers)
        return {'status': 200}
