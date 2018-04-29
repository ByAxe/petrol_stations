import psycopg2
from flask import Flask, g, request
from psycopg2.extras import DictCursor

from accounting.core.entities import Material, PetrolStation
from accounting.core.utils import json_response
from accounting.service.service import AccountingService

app = Flask(__name__)
accounting_service: AccountingService = None


@app.before_request
def before_request():
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


@app.route('/material/title/<string:title>', methods=['DELETE'])
def get_material(title):
    accounting_service.remove_material_by_title(title)
    return json_response()


@app.route('/material/id/<int:id>', methods=['DELETE'])
def get_material(id):
    accounting_service.remove_material_by_id(id)
    return json_response()


@app.route('/petrolstation', methods=['POST'])
def create_petrol_station():
    # Extract incoming params from request
    params = request.get_json()

    materials = [PetrolStation(param) for param in params]
    accounting_service.create_materials(materials)

    return json_response()
