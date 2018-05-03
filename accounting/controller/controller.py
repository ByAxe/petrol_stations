import psycopg2
from flask import Flask, g, request
from psycopg2.extras import DictCursor

from accounting.core.entities import Material, PetrolStation
from accounting.core.utils import json_response
from accounting.service.service import AccountingService

app = Flask(__name__)
accounting_service: AccountingService = None


@app.before_first_request
def before_first_request():
    """
    Initializes everything before the first request
    Works similar to post-construct phase in Java
    """
    g.connection = psycopg2.connect(app.config['DATABASE_NAME'])
    g.cur = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    global accounting_service
    accounting_service = AccountingService(g.connection, g.cur)


@app.route('/material', methods=['POST'])
def create_materials():
    # Extract incoming params from request
    params = request.get_json()

    materials = [Material(param) for param in params]
    accounting_service.create_materials(materials)

    return json_response()


@app.route('/material/<int:id>', methods=['GET'])
def get_material(id):
    material = accounting_service.get_material(id)
    return json_response(str(material))


@app.route('/material', methods=['GET'])
def get_materials():
    materials = accounting_service.get_materials()
    return json_response(str(materials))


@app.route('/material/<int:id>', methods=['DELETE'])
def remove_material(id):
    accounting_service.remove_material_by_id(id)
    return json_response()


@app.route('/petrolstation', methods=['POST'])
def create_petrol_station():
    # Extract incoming params from request
    params = request.get_json()

    materials = [PetrolStation(param) for param in params]
    accounting_service.create_materials(materials)

    return json_response()


@app.route('/petrolstation/<int:id>', methods=['DELETE'])
def remove_petrol_station(id):
    accounting_service.remove_petrol_station(id)
    return json_response()


@app.route('/petrolstation/<int:id>', methods=['GET'])
def get_petrol_station(id):
    petrol_station = accounting_service.get_petrol_station(id)
    return json_response(str(petrol_station))


@app.route('/petrolstation', methods=['GET'])
def get_petrol_stations():
    petrol_stations = accounting_service.get_petrol_stations()
    return json_response(str(petrol_stations))
