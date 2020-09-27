from flask import Flask
from flask_restful import Api
from flask_interface import *
app = Flask(__name__)
api = Api(app)
api.add_resource(Ordering, '/rayan')
api.add_resource(Tadbir, '/tadbir')

api.add_resource(nahayat_negar, '/nahayat_negar')

