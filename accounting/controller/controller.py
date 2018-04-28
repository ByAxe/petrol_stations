import psycopg2
from flask import Flask, g, request
from psycopg2.extras import DictCursor

from accounting.core.entities import Material
from accounting.service.service import create_materials, PetrolStationService

app = Flask(__name__)
petrolStationService: PetrolStationService = None


@app.before_request
def before_request():
    """
    Initializes everything before the first request
    Works similar to post-construct phase in Java
    """
    g.connection = psycopg2.connect(app.config['DATABASE_NAME'])
    g.cur = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    global petrolStationService
    petrolStationService = PetrolStationService(g.connection, g.cur)


@app.route('/material', methods=['POST'])
def load_chart_data():
    # Extract incoming params from request
    params = request.get_json()

    materials = [Material(param) for param in params]
    create_materials(materials)

    return json_response(str(r))


@app.route('/public/chartdata', methods=['DELETE'])
def deleteChartData():
    main_currency = request.args['main_currency'] if 'main_currency' in request.args else None
    secondary_currency = request.args['secondary_currency'] if 'secondary_currency' in request.args else None
    start = request.args['start'] if 'start' in request.args else None
    end = request.args['end'] if 'end' in request.args else None
    period = request.args['period'] if 'period' in request.args else None

    poloniexPublicService.deleteChartData(main_currency, secondary_currency, start, end, period)

    return json_response()
