from psycopg2.extras import DictCursor

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
        sql = "SELECT * FROM accounting.materials WHERE id = %s"
        self.cursor.execute(sql, str(id))
        material = self.cursor.fetchall()[0]
        return material

    def get_materials(self) -> list:
        sql = "SELECT * FROM accounting.materials"
        self.cursor.execute(sql)
        materials = self.cursor.fetchall()
        return materials

    def remove_material(self, id):
        sql = "DELETE FROM accounting.materials WHERE id = %s"

        self.cursor.execute(sql, str(id))

        self.connection.commit()

    def create_materials(self, materials: list):
        sql = "EXECUTE material_insert_plan (%s, %s, %s)"

        # actual insert into DB
        for material in materials:
            self.cursor.execute(sql, (material.title, material.description, material.cost))

        self.connection.commit()

    def remove_petrol_station(self, id):
        sql = "DELETE FROM accounting.petrol_stations WHERE id = %s"

        self.cursor.execute(sql, id)

        self.connection.commit()

    def create_petrol_stations(self, petrol_stations: list):
        sql = "EXECUTE station_insert_plan (%s, %s)"

        # actual insert into DB
        for petrol_station in petrol_stations:
            self.cursor.execute(sql, (petrol_station.title,
                                      petrol_station.location))

        self.connection.commit()

    def get_petrol_station(self, id):
        sql = "SELECT * FROM accounting.petrol_stations WHERE id = %s"
        self.cursor.execute(sql, id)
        petrol_station = self.cursor.fetchall()
        return petrol_station

    def get_petrol_stations(self):
        sql = "SELECT * FROM accounting.petrol_stations"
        self.cursor.execute(sql)
        petrol_stations = self.cursor.fetchall()
        return petrol_stations

    def get_materials_on_petrol_station(self, petrol_station_id):
        self.cursor.execute("SELECT * FROM accounting.materials_stations WHERE petrol_station_id = %s",
                            petrol_station_id)

        response: list = self.cursor.fetchall()

        return response

    def get_material_on_petrol_station(self, petrol_station_id, material_id) -> list:
        self.cursor.execute(
            "SELECT * FROM accounting.materials_stations WHERE petrol_station_id = %s AND material_id = %s",
            (petrol_station_id, material_id))

        response: list = self.cursor.fetchall()

        return response

    def take_material_from_petrol_station(self, petrol_station_id, material_id, number):
        materials_on_petrol_station = self.get_materials_on_petrol_station(petrol_station_id, material_id)

        if not materials_on_petrol_station:
            return "Nothing was taken. Current petrol station does not have any number of this material"
        else:
            sql = "EXECUTE materials_stations_update_number_plan (%s, %s, %s)"

            resulting_number = materials_on_petrol_station[0]['number'] - float(number)
            if resulting_number < 0:
                self.remove_material_from_petrol_station(petrol_station_id, material_id)
            else:
                self.cursor.execute(sql, (resulting_number, material_id, petrol_station_id))

        self.connection.commit()

    def add_material_to_petrol_station(self, petrol_station_id, material_id, number):
        materials_on_petrol_station = self.get_material_on_petrol_station(petrol_station_id, material_id)

        # If there is already present target material on station --> update amount
        if materials_on_petrol_station:
            sql = "EXECUTE materials_stations_update_number_plan (%s, %s, %s)"
            resulting_number = float(number) + materials_on_petrol_station[0]['number']
            self.cursor.execute(sql, (resulting_number, material_id, petrol_station_id))

        # Insert record
        else:
            sql = "EXECUTE materials_stations_insert_plan (%s, %s, %s)"

            self.cursor.execute(sql, (material_id, petrol_station_id, number))

        self.connection.commit()

    def remove_material_from_petrol_station(self, petrol_station_id, material_id):
        sql = "DELETE FROM accounting.materials_stations WHERE petrol_station_id = %s AND material_id = %s"

        self.cursor.execute(sql, (material_id, petrol_station_id))

        self.connection.commit()
