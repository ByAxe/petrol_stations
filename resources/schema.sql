DROP SCHEMA IF EXISTS accounting CASCADE;
CREATE SCHEMA accounting;

COMMENT ON SCHEMA accounting
IS 'Schema that contains all the data for interacting with petrol station API';

SET SEARCH_PATH TO accounting;

DROP TABLE IF EXISTS accounting.materials CASCADE;
CREATE TABLE accounting.materials (
  id          BIGSERIAL PRIMARY KEY,
  title       VARCHAR(30),
  description TEXT,
  cost        NUMERIC
);

DROP TABLE IF EXISTS accounting.petrol_stations CASCADE;
CREATE TABLE accounting.petrol_stations (
  id       BIGSERIAL PRIMARY KEY,
  title    VARCHAR(30),
  location TEXT
);

DROP TABLE IF EXISTS accounting.materials_stations CASCADE;
CREATE TABLE accounting.materials_stations (
  material_id       BIGINT REFERENCES accounting.materials,
  petrol_station_id BIGINT REFERENCES accounting.petrol_stations,
  date_of_incoming  TIMESTAMP DEFAULT now(),
  number            FLOAT
);

