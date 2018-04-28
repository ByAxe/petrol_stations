DROP SCHEMA IF EXISTS accounting CASCADE;
CREATE SCHEMA accounting;

COMMENT ON SCHEMA accounting IS 'Schema that contains all the data for interacting with petrol station API';

SET SEARCH_PATH TO accounting;

DROP TABLE IF EXISTS accounting.materials CASCADE;
CREATE TABLE accounting.materials (
  title           VARCHAR(30),
  description     TEXT,
  cost            NUMERIC
);

DROP TABLE IF EXISTS accounting.petrol_stations CASCADE;
CREATE TABLE accounting.petrol_stations (
  title           VARCHAR(30),
  location        TEXT,
  materials       NUMERIC
);

