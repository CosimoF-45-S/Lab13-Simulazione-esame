from database.DB_connect import DBConnect
from model import State



class DAO():

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
    def getEdges(year, days, idMap):
        cnx = DBConnect.get_connection()
        cursor1 = cnx.cursor()
        query1 = """select n.state1, n.state2, count(*) as peso  from neighbor n, sighting s1, sighting s2
                    where  year(s1.`datetime`) = %s and year(s2.`datetime`) = %s and s2.state = n.state2 and n.state1 < n.state2 
                    and s1.state = n.state1 and ABS(datediff(s1.`datetime`, s2.`datetime`)) <= %s group by n.state1, n.state2"""
        cursor1.execute(query1, (year, year, days))
        rows = cursor1.fetchall()
        result = []
        for row in rows:
            result.append((idMap[row[0]], idMap[row[1]], row[2]))
        cursor1.close()

        cnx.close()
        return result


