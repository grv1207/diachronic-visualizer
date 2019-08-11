
from  mysql.connector import connection
from mysql.connector import errorcode

import numpy as np
import io

class DatabaseConnection():

    def __init__(self,concept_ID,semantic_type):
        self.concept_ID = concept_ID
        self.semantic_type = semantic_type
        self.time_frame = ['1809_1970', '1971_1975', '1976_1980', '1981_1985', '1986_1990', '1991_1995', '1996_2000',
                          '2001_2005','2006_2010', '2011_2012', '2013_2015']
        try:

            self.cnx = connection.MySQLConnection(user='root', password='12345678',
                                          host='127.0.0.1',
                                          database='DB_embedding')
            #self.cnx.query('SET GLOBAL connect_timeout=28800')
            #self.cnx.query('SET GLOBAL wait_timeout=28800')
            #self.cnx.query('SET GLOBAL interactive_timeout=28800')
        except connection.errors as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        self.cursor = self.cnx.cursor()
        self.dict = {}

    def get_nearest_neighbour(self):
        top_n_neighbor_per_period = {}
         # chnage this tabke
        for time in self.time_frame:
            top_n_neighbor_per_period[time] = self.top_n_similar(self.concept_ID,time)

        return top_n_neighbor_per_period

    def top_n_similar(self,concept, table, topN=3):
        lower_dict ={}
        similarity_list = []
        query_all = "select  * from t_{} ".format(table)
        self.cursor.execute(query_all)
        for value in  self.cursor.fetchall() :
            lower_dict[value[0]] = np.array(value[1:],dtype=np.float64)#self.convert_array()

        if concept in lower_dict:
            embedding_for_given_concept =  lower_dict[concept]

            for concept_key,embedding_value in lower_dict.items():
                if concept != concept_key:
                    similarity_list.append((concept_key,self.get_cosine_score(embedding_for_given_concept,embedding_value)))

            # get top N similar concepts for the given input concept
            self.close_connection()

            return sorted(similarity_list,key=lambda x: x[1],reverse=True)[:topN]


        else:
            self.close_connection()
            # when concept in not in the given table
            return None


    def close_connection(self):
        self.cursor.close()
        self.cnx.close()


    def get_cosine_score(self, embedding_one, embedding_two):
        """
         returns the normalized cosine similarity between two vector, similar to gensim consine similarity
        """
        vec1 = self.convert_array(embedding_one)
        vec2 = self.convert_array(embedding_two)

        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))



    def convert_array(self,blob):
        """
        Using BytesIO to convert the binary version of the array back into a numpy array.
        """
        out = io.BytesIO(blob)
        out.seek(0)

        return np.load(out)
