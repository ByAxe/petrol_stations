MATERIALS_INSERT_PLAN_SQL = """
PREPARE material_insert_plan AS
    INSERT INTO accounting.materials
    (title, description, cost)
    VALUES ($1, $2, $3)"""

STATIONS_INSERT_PLAN_SQL = """
PREPARE material_insert_plan AS
    INSERT INTO accounting.petrol_stations
    (title, location, materials)
    VALUES ($1, $2, $3)"""
