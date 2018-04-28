DROP SCHEMA IF EXISTS accounting CASCADE;
CREATE SCHEMA accounting;

COMMENT ON SCHEMA accounting IS 'Schema that contains all the data for interacting with petrol station API';

SET SEARCH_PATH TO accounting;

DROP TABLE IF EXISTS accounting.materials CASCADE;
CREATE TABLE materials (
  id              BIGSERIAL PRIMARY KEY,
  title           VARCHAR(30),
  description     TEXT,
  cost            NUMERIC
);

DROP TABLE IF EXISTS accounting.petrol_stations CASCADE;
CREATE TABLE petrol_stations (
  id              BIGSERIAL PRIMARY KEY,
  title           VARCHAR(30),
  location        TEXT,
  materials       NUMERIC
);

