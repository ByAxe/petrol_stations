import calendar
import datetime

from flask import make_response

JSON_MIME_TYPE = 'application/json'

MATERIALS_INSERT_PLAN_SQL = """
PREPARE material_insert_plan AS
    INSERT INTO accounting.materials
    (title, description, cost)
    VALUES ($1, $2, $3)"""

STATIONS_INSERT_PLAN_SQL = """
PREPARE station_insert_plan AS
    INSERT INTO accounting.petrol_stations
    (title, location)
    VALUES ($1, $2, $3)"""

MATERIALS_STATIONS_INSERT_PLAN_SQL = """
PREPARE materials_stations_insert_plan AS
    INSERT INTO accounting.materials_stations
    (material_id, petrol_station_id, number)
    VALUES ($1, $2, $3)"""

MATERIALS_STATIONS_UPDATE_NUMBER_PLAN_SQL = """
PREPARE materials_stations_update_number_plan AS
    UPDATE accounting.materials_stations 
    SET number = $1 
    WHERE material_id = $2 AND petrol_station_id = $3"""


def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)


def datetime_to_timestamp(date_time: datetime):
    return str(calendar.timegm(date_time.timetuple()))
