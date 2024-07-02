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
    def getShapes(year):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """ select distinct s.shape  from sighting s where year(s.`datetime`) = %s """
        cursor.execute(query, (year, ))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row[0])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getStates():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)
        query = """ select * from state s """
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(State.State(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getWeight(node1, node2, shape, year):
        cnx = DBConnect.get_connection()
        cursor1 = cnx.cursor()
        query1 = """select count(*) from neighbor n where (n.state1 = %s and n.state2=%s)"""
        cursor1.execute(query1, (node1, node2))
        row1 = cursor1.fetchone()
        cursor1.close()
        if row1[0] == 1:
            cursor2 = cnx.cursor()
            query2 = """select count(*) from sighting s where year(s.`datetime`) = %s and s.shape = %s and (s.state = %s or s.state = %s)"""
            cursor2.execute(query2, (year, shape, node1, node2))
            row = cursor2.fetchone()
            cursor2.close()
            cnx.close()
            return row[0]

        cnx.close()
        return -1

    @staticmethod
    def getEdges(shape, year, idMap):
        cnx = DBConnect.get_connection()
        cursor1 = cnx.cursor()
        query1 = """select n.state1, n.state2, count(*) as peso  from neighbor n, sighting s1
                    where  year(s1.`datetime`) = %s and (s1.state = n.state2 
                    or s1.state = n.state1) and s1.shape = %s group by n.state1, n.state2"""
        cursor1.execute(query1, (year, shape))
        rows = cursor1.fetchall()
        result = []
        for row in rows:
            result.append([idMap[row[0]], idMap[row[1]], row[2]])
        cursor1.close()

        cnx.close()
        return result

