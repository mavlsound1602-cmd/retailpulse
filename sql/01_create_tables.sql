-- RetailPulse: Create Tables
-- Run once to load all CSVs into DuckDB

CREATE OR REPLACE TABLE raw_train AS SELECT * FROM read_csv_auto('data/train.csv');
CREATE OR REPLACE TABLE raw_stores AS SELECT * FROM read_csv_auto('data/stores.csv');
CREATE OR REPLACE TABLE raw_items AS SELECT * FROM read_csv_auto('data/items.csv');
CREATE OR REPLACE TABLE raw_oil AS SELECT * FROM read_csv_auto('data/oil.csv');
CREATE OR REPLACE TABLE raw_holidays AS SELECT * FROM read_csv_auto('data/holidays_events.csv');
CREATE OR REPLACE TABLE abc_xyz AS SELECT * FROM read_csv_auto('data/abc_xyz_classification.csv');
CREATE OR REPLACE TABLE business_outputs AS SELECT * FROM read_csv_auto('data/business_outputs.csv');
