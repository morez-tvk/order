from flask import Flask
from flask_restful import Api
from flask_interface import set_order, nahayat_negar, Tadbir , chogan , datax_oms

app = Flask(__name__)
api = Api(app)
api.add_resource(set_order, '/ordering')
api.add_resource(nahayat_negar, '/nahayat_negar')
api.add_resource(Tadbir, '/tadbir')
api.add_resource(chogan, '/chogan')
api.add_resource(datax_oms, '/datax')
