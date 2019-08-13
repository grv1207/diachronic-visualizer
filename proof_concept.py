
import numpy as np
import tables as tb


TIME_FRAME = ['1809_1970', '1971_1975', '1976_1980', '1981_1985', '1986_1990', '1991_1995', '1996_2000','2001_2005','2006_2010','2011_2012','2013_2015']
class pairwise_similarity():
    def __init__(self,concept1,concept2):
        self.concept1 = concept1
        self.concept2 = concept2

    def get_SGNS_score(self):
        """

        :return: SGNS between two concepts using cosine score
        """
        similarity = []
        H5FILE = tb.open_file("../model_vec/embedding_index_DB.h5", mode="r",
                            title="embedding DB")
        try:
            for time in TIME_FRAME:
                score=0
                table_node = H5FILE.get_node('/embedding_group/'+time) #C0021344, C0282515

                for first_concept in table_node.where('concepts == b"' +  self.concept1  + '"'):
                    embedding_for_first_concept = np.array(first_concept['embedding'], dtype=np.float64)

                    for second_concept in table_node.where('concepts == b"' +  self.concept2  + '"'):
                        embedding_for_second_concept = np.array(second_concept['embedding'], dtype=np.float64)

                        score = self.get_cosine_score(embedding_for_first_concept,embedding_for_second_concept)

                similarity.append(score)



        except Exception as e :
            H5FILE.close()
            print(e)


        finally:
            H5FILE.close()

        return similarity

    def get_PPMI_score(self):
        """

        :return: PPPMI between two concepts using cosine score
        """
        return ""


    def get_raw_score(self):
        """

        :return: raw corpus count
        """
        return""


    def get_cosine_score(self, vec1, vec2):
        """
         returns the normalized cosine similarity between two vector, similar to gensim consine similarity
        """

        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

