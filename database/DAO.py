from database.DB_connect import DBConnect
from model import State



class DAO():

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """ select distinct YEAR(`datetime`) from sighting s """
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row[0])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getNumAvv(year):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """ select count(*) from (select distinct s.id from sighting s
                    where year(s.datetime) = %s) as sub  """
        cursor.execute(query, (year, ))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()
        return row[0]

    @staticmethod
    def getNodes(year):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)
        query = """select  id, Name, Capital, Lat, Lng, Area, Population, Neighbors
                    from state, (select distinct s.state from sighting s where year(s.`datetime`) = %s)
                    sid where id = sid.state """
        cursor.execute(query, (year, ))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(State.State(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getEdges(year, idMap):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """select distinct s1.state as st1, s2.state as st2 from sighting s1, sighting s2 where s2.state <> s1.state 
                    and year(s1.`datetime`) = %s and year(s2.`datetime`) = %s and s2.`datetime` > s1.`datetime` """
        cursor.execute(query, (year, year))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append([idMap[row[0].upper()], idMap[row[1].upper()]])
        cursor.close()
        cnx.close()
        return result

