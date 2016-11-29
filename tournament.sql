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

-- Make a new table
CREATE TABLE players (
	player_id serial,
	player_name text,
	PRIMARY KEY(player_id));

--This table records all matches with a unique ID, and the winner/loser
CREATE TABLE matches (
	match_id serial,
	winning_player integer references players(player_id),
	losing_player integer references players(player_id));
	
-- Orders players from most to least number of wins
CREATE VIEW player_wins 
	AS SELECT players.player_id as player_id, count(matches.winning_player) as wins 
	FROM players LEFT JOIN matches 
	ON player_id = matches.winning_player 
	GROUP BY players.player_id;
	
-- Counts how many maches each player has played
CREATE VIEW player_matches 
	AS SELECT players.player_id as player_id, count(matches) AS matches
	FROM players LEFT JOIN matches 
	ON  (players.player_id = matches.losing_player) 
	OR (players.player_id = matches.winning_player) 
	GROUP BY players.player_id
	ORDER BY players.player_id DESC;

-- A view containing player_id, player_name, total_wins, total_matches:
CREATE VIEW player_standings
	AS SELECT players.player_id, players.player_name,
	player_wins.wins, player_matches.matches
	FROM players, player_wins, player_matches
	WHERE player_wins.player_id = players.player_id
	AND players.player_id = player_matches.player_id
	ORDER BY wins DESC;
