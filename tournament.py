#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

# set the current tournament to the first id in table
tournament_id = 1

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    con = connect()
    cur = con.cursor()
    query = "DELETE FROM matches"
    cur.execute(query)
    con.commit()
    con.close()


def deletePlayers():
    """Remove all the player records from the database."""
    con = connect()
    cur = con.cursor()
    query = "DELETE FROM players"
    cur.execute(query)
    con.commit()
    con.close()

def countPlayers():
    """Returns the number of players currently registered."""
    con = connect()
    cur = con.cursor()
    query = "SELECT count(*) from players"
    cur.execute(query)
    counter = cur.fetchone()[0]
    con.close()
    return counter


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    con = connect()
    cur = con.cursor()
    player_name = bleach.clean(name, strip=True)
    query = "INSERT INTO players (name) values (%s)"
    cur.execute(query, (player_name,))
    con.commit()
    con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    con = connect()
    cur = con.cursor()
    query = "SELECT * FROM standings;"
    cur.execute(query)
    results = cur.fetchall()
    con.commit()
    con.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    con = connect()
    cur = con.cursor()
    query = "INSERT INTO matches (winner, loser) values (%s, %s)"
    cur.execute(query, (winner, loser,))
    con.commit()
    con.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    con = connect()
    cur = con.cursor()
    query = "SELECT * FROM standings;"
    cur.execute(query)
    results = cur.fetchall()
    pairings = []
    count = len(results)

    for x in range(0, count - 1, 2):
        paired_list = (results[x][0], results[x][1], results[x + 1][0], results[x + 1][1])
        pairings.append(paired_list)

    con.close()
    return pairings

