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
