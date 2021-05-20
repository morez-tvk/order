from flask import Flask, request, jsonify
import requests
from nahayat import NahayatNegar
import flask
import time
from multiprocessing import Process
import json
from LogMg import logger

# import requests
app = Flask(__name__)
app.config["DEBUG"] = True
import datetime


def input_validator(request):
    try:
        text_json = request.data
        json.loads(text_json)
    except:
        return False
    return True


oid = 0
orders = {}
l_o = {}
session = requests.Session()


@app.route('/nahayat_negar', methods=['post'])
def first_order():
    global oid
    global l_o
    global orders
    if not input_validator(request):
        flask.abort(400, "The input should be json.")
    text_json = request.data
    data = json.loads(text_json)
    if data['status'] == 'set':
        oid += 1
        # time_period = data.get('tedad', 20)
        # delay = data.get('delay', 0)
        next_ot = data.get("next_ot")
        orders[oid] = NahayatNegar(data=data['json'], limit_time=data['time'],
                                   servers=data['servers'])
        orders[oid].order(next_ot)
        # t = Process(target=orders[oid].order, args=(next_ot))
        # t.start()
        print("wating ...")
        # orders [oid].multi_req (delay, time_period)
        # l_o[oid] = t
        return {'id': oid, 'status': 200}

    elif data['status'] == 'cancel':
        try:
            l_o[data['id']].terminate()
            l_o[data['id']].join(0)
            orders.pop(data['id'])
            return {"message": f"order {data['id']} deleted from queue"}
        except:
            flask.abort(500, "No such order in queue")


@app.route('/get_next', methods=['post'])
def x():
    req = request.json
    logger.info('sending request')
    try:
        res = requests.post(req['link'], cookies=req['cookies'], headers=req['headers'], data=req['data'])
        ot = res.json()['customer']['orderTicket']
        req['data']['data']['orderTicket'] = ot
    except KeyError:
        logger.error(res.json())
    except Exception as e:
        logger.error('whattttttttt')

    if req['counter'] + 1 < len(req['servers']):
        logger.info("sending to next one")
        session.post(f"{req['servers'][req['counter']]}:2021/get_next", json={
            "link": req['link'],
            "cookies": req['cookies'],
            "headers": req['headers'],
            "data": json.dumps(req['data']),
            "servers": req['servers'],
            "counter": req['counter'] + 1
        })
    try:
        logger.info(res.json())
    except Exception as e:
        pass


app.run(host='localhost',port=2020)
