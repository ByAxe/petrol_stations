from accounting.core.utils import STATIONS_INSERT_PLAN_SQL, MATERIALS_INSERT_PLAN_SQL


class PetrolStationService:
    connection = None
    cursor = None

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        # prepares the query for insert
        self.cursor.execute(MATERIALS_INSERT_PLAN_SQL)

        # prepares the query for insert
        self.cursor.execute(STATIONS_INSERT_PLAN_SQL)

        self.connection.commit()

    def create_materials(self, materials: list):
        sql = "EXECUTE material_insert_plan (%s, %s, %s)"

        # actual insert into DB
        for material in materials:
            self.cursor.execute(sql, (material['title'],
                                      material['description'],
                                      material['cost']))

        self.connection.commit()

    def create_petrol_station(self, petrol_stations: list):
        sql = "EXECUTE station_insert_plan (%s, %s, %s)"

        # actual insert into DB
        for petrol_station in petrol_stations:
            self.cursor.execute(sql, (petrol_station['title'],
                                      petrol_station['location'],
                                      petrol_station['materials']))

        self.connection.commit()
