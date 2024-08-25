import sqlite3
import pandas as pd
from sympy.polys.polyconfig import query


class sql_py:
    def __init__(self):
        conn = sqlite3.connect("my_database.db")
        self.cursor = conn.cursor()

    def batter_find(self, style, position, matches, sr, avg, boundary):
        self.query = """
        SELECT * FROM batters
        WHERE battingStyle = ? AND Batting_Position <= ? AND Matches >= ?
        AND Strike_Rate >= ? AND Batting_Average >= ? AND `Boundary%` >= ?
        """
        self.cursor.execute(self.query, (style, position, matches, sr, avg, boundary))
        data = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        df = pd.DataFrame(data, columns=columns)
        return df.head()
    def all_rounder_find(self,position,matches_batted,bt_sr,bt_avg,matches_bowled,economy,bw_sr):
        self.query = """
        SELECT * FROM all_rounders
        WHERE Innings_batted >= ? AND Batting_Position <= ? AND Economy <= ? AND Bowling_Sr <= ?
        AND Batting_Average >= ? AND Batting_Sr >= ? AND Innings_bowled >= ?
        """
        self.cursor.execute(self.query, (matches_batted,position,economy,bw_sr,bt_avg,bt_sr,matches_bowled))
        data = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        df = pd.DataFrame(data, columns=columns)
        return df.head()
    def bowlers_find(self,style,avg,matches,economy,sr):
        if style == 'Fast':
            self.query = """
            SELECT * FROM bowlers
            WHERE (bowlingStyle LIKE '%Fast%' OR bowlingStyle LIKE '%fast%') AND Matches >= ? AND Economy <= ? AND strike_rate <= ? AND Bowling_Average <= ?
            """
        else:
            self.query = """
            SELECT * FROM bowlers
            WHERE bowlingStyle NOT LIKE '%Fast%' AND bowlingStyle NOT LIKE '%fast%' AND Matches >= ? AND Economy <= ? AND strike_rate <= ? AND Bowling_Average <= ?
            """
        self.cursor.execute(self.query,(matches,economy,sr,avg))
        data = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        df = pd.DataFrame(data,columns = columns)
        return df.head()