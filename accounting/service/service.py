from psycopg2.extras import DictCursor

from accounting.core.entities import Material, PetrolStation
from accounting.core.utils import *


class AccountingService:
    connection = None
    cursor: DictCursor = None

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        # prepare the queries
        self.cursor.execute(MATERIALS_INSERT_PLAN_SQL)
        self.cursor.execute(STATIONS_INSERT_PLAN_SQL)
        self.cursor.execute(MATERIALS_STATIONS_INSERT_PLAN_SQL)
        self.cursor.execute(MATERIALS_STATIONS_UPDATE_NUMBER_PLAN_SQL)

        self.connection.commit()

    def get_material(self, id):
        sql = "SELECT * FROM accounting.materials WHERE id = %i"
        self.cursor.execute(sql, id)
        material = self.cursor.fetchall()
        return Material(material)

    def get_materials(self):
        sql = "SELECT * FROM accounting.materials"
        self.cursor.execute(sql)
        materials = self.cursor.fetchall()
        return [Material(material) for material in materials]

    def remove_material_by_id(self, title):
        sql = "DELETE FROM accounting.materials WHERE title = %s"

        self.cursor.execute(sql, title)

        self.connection.commit()

    def create_materials(self, materials: list):
        sql = "EXECUTE material_insert_plan (%s, %s, %s)"

        # actual insert into DB
        for material in materials:
            self.cursor.execute(sql, (material.title, material.description, material.cost))

        self.connection.commit()

    def remove_petrol_station(self, id):
        sql = "DELETE FROM accounting.petrol_stations WHERE id = %i"

        self.cursor.execute(sql, id)

        self.connection.commit()

    def create_petrol_stations(self, petrol_stations: list):
        sql = "EXECUTE station_insert_plan (%s, %s)"

        # actual insert into DB
        for petrol_station in petrol_stations:
            self.cursor.execute(sql, (petrol_station['title'],
                                      petrol_station['location']))

        self.connection.commit()

    def get_petrol_station(self, id):
        sql = "SELECT * FROM accounting.petrol_stations WHERE id = %i"
        self.cursor.execute(sql, id)
        petrol_station = self.cursor.fetchall()
        return PetrolStation(petrol_station)

    def get_petrol_stations(self):
        sql = "SELECT * FROM accounting.petrol_stations"
        self.cursor.execute(sql)
        petrol_stations = self.cursor.fetchall()
        return [PetrolStation(petrol_station) for petrol_station in petrol_stations]

    def get_materials_on_petrol_station(self, petrol_station_id, material_id) -> list:
        self.cursor.execute(
            "SELECT * FROM accounting.materials_stations WHERE petrol_station_id = %i AND material_id = %i",
            (petrol_station_id, material_id))

        response: list = self.cursor.fetchall()

        return response

    def take_material_from_petrol_station(self, petrol_station_id, material_id, number):
        materials_on_petrol_station = self.get_materials_on_petrol_station(petrol_station_id, material_id)

        if not materials_on_petrol_station:
            return "Nothing was taken. Current petrol station does not have any number of this material"
        else:
            sql = "EXECUTE materials_stations_update_number_plan (%f, %i, %i)"

            resulting_number = float(materials_on_petrol_station[0]['number']) - number
            if resulting_number < 0:
                self.remove_material_from_petrol_station(petrol_station_id, material_id)
            else:
                self.cursor.execute(sql, (resulting_number, material_id, petrol_station_id))

        self.connection.commit()

    def add_material_to_petrol_station(self, petrol_station_id, material_id, number):
        materials_on_petrol_station = self.get_materials_on_petrol_station(petrol_station_id, material_id)

        # If there is already present target material on station --> update amount
        if materials_on_petrol_station:
            sql = "EXECUTE materials_stations_update_number_plan (%f, %i, %i)"
            resulting_number = number + float(materials_on_petrol_station[0]['number'])
            self.cursor.execute(sql, (resulting_number, material_id, petrol_station_id))

        # Insert record
        else:
            sql = "EXECUTE materials_stations_insert_plan (%i, %i, %f)"

            self.cursor.execute(sql, (material_id, petrol_station_id, number))

        self.connection.commit()

    def remove_material_from_petrol_station(self, petrol_station_id, material_id):
        sql = "DELETE FROM accounting.materials_stations WHERE petrol_station_id = %i AND material_id = %i"

        self.cursor.execute(sql, (material_id, petrol_station_id))

        self.connection.commit()
