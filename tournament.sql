-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Creation of tournament db

-- Delete existing database
DROP DATABASE IF EXISTS tournament;

-- Make a new Database
CREATE DATABASE tournament;

-- Connect to database
\c tournament

-- Delete existing table
DROP TABLE IF EXISTS tour_table;

-- Make a new table
CREATE TABLE tour_table (
	player_id serial,
	player_name text,
	wins integer,
	matches integer);


