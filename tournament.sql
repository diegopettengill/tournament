-- Drop the database for a clean install
DROP DATABASE IF EXISTS tournament;

-- Creates our database
CREATE DATABASE tournament;

-- Connects to it
\connect tournament

-- Drop the following tables if they exists
DROP TABLE IF EXISTS player CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS standings CASCADE;

-- Creates our players table
CREATE TABLE players (
  id serial PRIMARY KEY,
  name VARCHAR (100) NOT NULL
);

-- Creates our matches table
CREATE TABLE matches (
  id serial PRIMARY KEY,
  winner INTEGER,
  loser INTEGER,
  FOREIGN KEY (winner) REFERENCES players(id),
  FOREIGN KEY (loser) REFERENCES players(id)
);

-- Creates a view to show the players standings
CREATE VIEW standings AS
  SELECT p.id as player_id, p.name,
  (SELECT count(*) FROM matches WHERE matches.winner = p.id) as won,
  (SELECT count(*) FROM matches WHERE p.id in (winner, loser)) as played
  FROM players p
GROUP BY p.id
ORDER BY won DESC;