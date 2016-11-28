#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    # set all win and match records to 0
    cur.execute("""UPDATE tour_table SET wins=0, matches=0
                   WHERE matches!=0;""")
    conn.commit()
    cur.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    # Remove all rows from table
    cur.execute("""DELETE FROM tour_table;""")
    conn.commit()
    cur.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    # count the number of rows in table
    cur.execute("SELECT COUNT(player_name) FROM tour_table;")
    count = int(cur.fetchone()[0])
    conn.close()
    return(count)


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    # creates a new entry with the name passed to the function
    SQL = """INSERT INTO tour_table (player_name, matches, wins)
             VALUES (%s, 0, 0);"""
    data = (name,)
    cur.execute(SQL, data)
    conn.commit()
    cur.close()
    conn.close()


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
    conn = connect()
    cur = conn.cursor()
    # get a tuple of all the players ranked in order of most wins
    cur.execute("""SELECT player_id, player_name, wins, matches FROM tour_table
                   ORDER BY wins DESC;""")
    standings = cur.fetchall()
    cur.close()
    conn.close()
    return(standings)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    # get a tuple containing the number of wins and matches for the winner
    cur.execute("SELECT wins, matches FROM tour_table where player_id=(%s);",
                (winner,))
    winner_update = cur.fetchone()
    winner_wins = int(winner_update[0]) + 1
    winner_matches = int(winner_update[1]) + 1
    # increment the number of wins and matches for winner by one
    cur.execute("""UPDATE tour_table SET wins=(%s), matches=(%s)
                WHERE player_id=(%s);""",
                (winner_wins, winner_matches, winner,))
    conn.commit()
    # get a tuple containing the number of wins and matches for the loser
    cur.execute("SELECT matches FROM tour_table where player_id=(%s)",
                (loser,))
    matches_update = cur.fetchone()
    loser_matches = int(matches_update[0]) + 1
    # increment the number of matches for the loser by one
    cur.execute("""UPDATE tour_table SET matches=(%s) WHERE player_id=(%s)""",
                (loser_matches, loser, ))
    conn.commit()
    cur.close()
    conn.close()


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
    conn = connect()
    cur = conn.cursor()
    # get a tuple of all players in descending order of most wins
    cur.execute("""SELECT player_id, player_name FROM tour_table
                   ORDER BY wins DESC;""")
    ranking = cur.fetchall()
    number_players = len(ranking)
    counter = 0
    pairs_list = []
    #  take a list of players in order of wins, and split them into pairs
    while counter < number_players:
        player_a = counter
        counter += 1
        player_b = counter
        match = (ranking[player_a][0], ranking[player_a][1],
                 ranking[player_b][0], ranking[player_b][1], )
        pairs_list.append(match)
        counter += 1
    cur.close()
    conn.close()
    return(pairs_list)
