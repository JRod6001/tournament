#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("error trying to connect to DB")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()

    # Delete all rows from the matches table
    query = """TRUNCATE TABLE matches;"""
    cursor.execute(query)

    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    # Remove all rows from players table
    query = """TRUNCATE TABLE players, matches;"""
    cursor.execute(query)

    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    # query the number of players currently registered
    query = "SELECT COUNT(player_name) FROM players;"
    cursor.execute(query)
    count = int(cursor.fetchone()[0])

    db.close()
    return(count)


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    # creates a new entry with the name passed to the function
    SQL = """INSERT INTO players (player_name)
             VALUES (%s);"""
    data = (name,)
    cursor.execute(SQL, data)

    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()

    # This queries the data in the player_standings view
    query = """SELECT * from player_standings;"""
    cursor.execute(query)
    standings = cursor.fetchall()

    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    # enter into the matches table the winning and losing player for a match
    query = """INSERT INTO matches (winning_player, losing_player)
            VALUES (%s, %s);"""
    data = (winner, loser,)
    cursor.execute(query, data)

    db.commit()
    db.close()


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
    ranking = playerStandings()
    counter = 0
    number_players = len(ranking)
    pairs_list = []

    # This statement takes the list of tuples retrieved from playerStandings()
    # and returns a list of paired players
    while counter < number_players:
        player_a = counter
        counter += 1
        player_b = counter
        match = (ranking[player_a][0], ranking[player_a][1],
                 ranking[player_b][0], ranking[player_b][1], )
        pairs_list.append(match)
        counter += 1

    return(pairs_list)

