from accounting.core.utils import *


class AccountingService:
    connection = None
    cursor = None

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        # prepares the query for insert
        self.cursor.execute(MATERIALS_INSERT_PLAN_SQL)

        # prepares the query for insert
        self.cursor.execute(STATIONS_INSERT_PLAN_SQL)

        # prepares the query for insert
        self.cursor.execute(MATERIALS_STATIONS_INSERT_PLAN_SQL)

        self.connection.commit()

    def remove_material(self, title):
        sql = "DELETE FROM accounting.materials WHERE title = %s"

        self.cursor.execute(sql, title)

        self.connection.commit()

    def create_materials(self, materials: list):
        sql = "EXECUTE material_insert_plan (%s, %s, %s)"

        # actual insert into DB
        for material in materials:
            self.cursor.execute(sql, (material['title'],
                                      material['description'],
                                      material['cost']))

        self.connection.commit()

    def remove_petrol_station(self, title, location):
        sql = "DELETE FROM accounting.petrol_stations WHERE title = %s AND location = %s"

        self.cursor.execute(sql, (title, location))

        self.connection.commit()

    def create_petrol_station(self, petrol_stations: list):
        sql = "EXECUTE station_insert_plan (%s, %s)"

        # actual insert into DB
        for petrol_station in petrol_stations:
            self.cursor.execute(sql, (petrol_station['title'],
                                      petrol_station['location']))

        self.connection.commit()

    def take_material_from_petrol_station(self, petrol_station_id, material_id, number):

        pass

    def add_material_to_petrol_station(self, petrol_station_id, material_id, number):
        self.cursor.execute(
            "SELECT * FROM accounting.materials_stations WHERE petrol_station_id = %i AND material_id = %i",
            (petrol_station_id, material_id))

        response: list = self.cursor.fetchAll()

        # If there is already present target material on station --> update amount
        if response:
            sql = "UPDATE accounting.materials_stations SET number = %f WHERE material_id = %i AND petrol_station_id = %i"
            self.cursor.execute(sql, (number + float(response[0]['number']), material_id, petrol_station_id))

        # Insert record
        else:
            sql = "EXECUTE materials_stations_insert_plan (%i, %i, %f)"
            self.cursor.execute(sql, material_id, petrol_station_id, number)

        self.connection.commit()
