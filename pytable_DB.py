import time

from tables import *
import numpy as np
import pickle
import datetime
from operator import itemgetter
from urllib import request
#TOPN=3
#from multiprocess import Process, Manager
with open('data_dir_UI/semantic_conceptList.bin','rb') as fin:   #semantic_cui_name_dict
    SEMANTIC_DICT = pickle.load(fin)


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed

class PY_table_connection(object):

    def __init__(self,concept_ID,selected_semantic_type_list, top_neighbour):
        self.concept_ID = concept_ID
        self.top_neighbour = int(top_neighbour)
        self.neg_top_neighbour = -(self.top_neighbour+1)
        self.selected_semantic_type_list= selected_semantic_type_list
        self.time_frame = ['1809_1970', '1971_1975', '1976_1980', '1981_1985', '1986_1990', '1991_1995', '1996_2000',
                          '2001_2005','2006_2010', '2011_2012', '2013_2015']

        self.H5FILE = open_file("/Users/gauravvashisth/Documents/UNI-Folder/thesis/model_vec/embedding_index_DB.h5", mode="r", title="embedding DB")
        self.semantic_dict = SEMANTIC_DICT
        #self.concept_dict = concept_dict
        self.filter_concept_with_semantic_type()
    #@timeit
    def get_nearest_neighbour(self):
        top_n_neighbor_per_period = {}
         # chnage this tabke
        for time in self.time_frame: #C0023473 [:2] [:3]
            #start_time = datetime.datetime.now()
            table_node = self.H5FILE.get_node('/embedding_group/'+time) #+'t_'
            top_n_neighbor_per_period[table_node.name] = self.top_n_similar(self.concept_ID,table_node)
            #end_time = datetime.datetime.now()
            #t_delta = end_time - start_time
            #print("for {} reading time : {}".format(time,t_delta))

        self.H5FILE.close()
        return top_n_neighbor_per_period

    #@timeit
    def top_n_similar(self,concept, table):
        start_time = datetime.datetime.now()
        #concept_present = False

        #embedding_for_given_concept = ''
        get_embedding = itemgetter(*['embedding'])
        get_concept = itemgetter(*['concepts'])

        embedding_data = get_embedding(table.read())
        concept_data = get_concept(table.read())

        #for check_concept in table.where('concepts == b"'+concept+'"'):
            #concept_present = True
            #embedding_for_given_concept = np.array(check_concept['embedding'],dtype=np.float64)
            #break
        embedding_for_given_concept = embedding_data[np.where(concept_data==concept.encode())[0][0],:]


        if  len(embedding_for_given_concept)>0:
            np_need = embedding_for_given_concept.reshape(1, 300)
            #table_content = table.read()

            dot_product = np.dot(np_need, embedding_data.T)
            normalized_vec = np.multiply(np.linalg.norm(np_need, axis=1), np.linalg.norm(embedding_data, axis=1))
            np_cosine_result = np.divide(dot_product, normalized_vec)


            #top_n_result = np_cosine_result.ravel()[np_cosine_result.ravel().argsort()[-4:][::-1][1:]].tolist()
            #top_n_concept = concept[np_cosine_result.ravel().argsort()[-4:][::-1][1:]].tolist()

            top_n_result = np_cosine_result.ravel()[np_cosine_result.ravel().argsort()[::-1][1:]].tolist() #[self.neg_top_neighbour:]
            top_n_concept = concept_data[np_cosine_result.ravel().argsort()[::-1][1:]].tolist() #[self.neg_top_neighbour :]

            """for row in  table.where('concepts != b"'+concept+'"') :
                    similarity_list.append((row['concepts'],self.get_cosine_score(embedding_for_given_concept,np.array(row['embedding'],dtype=np.float64))))
            """
            end_time = datetime.datetime.now()
            t_delta = end_time - start_time
            similarity_list = [ (neighbour_concept, score) for neighbour_concept, score in zip(top_n_concept, top_n_result) ]

            print("PROCESSING TIME for reading table {} (sec): {}".format(table.name,t_delta.seconds))

            #return self.get_topN_neighbour(sorted(similarity_list,key=lambda x: x[1],reverse=True))
            return self.get_topN_neighbour(similarity_list)


        else:
            # when concept in not in the given table
            return None

    #@timeit
    def get_topN_neighbour(self, sorted_list):
        final_neighbor = []
        #start_time = datetime.datetime.now()
        for neighbor in sorted_list:
            if len(final_neighbor)== self.top_neighbour :
                break
            elif neighbor[0].decode() in self.filtered_concept:

                _name= self.get_concept_name(neighbor[0].decode())
                _semantic_type = self.get_semantic_type(neighbor[0].decode())
                final_neighbor.append((neighbor[0],neighbor[1],_name,_semantic_type))
        #end_time = datetime.datetime.now()
        #t_delta = end_time - start_time

        #print("PROCESSING TIME for get_topN_neighbour (sec): {}".format(t_delta.seconds))
        return final_neighbor

    def get_concept_name(self, conceptID):
        connection = request.urlopen(
            'http://127.0.0.1:8983/solr/MRCONSO/select?indent=on&q=IX_umlsCode:' + conceptID + '&wt=python')
        response = eval(connection.read())

        return response['response']['docs'][0]['IX_umlsName']


    def get_semantic_type(self,conceptID):
        connection = request.urlopen(
            'http://127.0.0.1:8983/solr/SEMANTIC_TYPE/select?indent=on&q=IX_umlsConceptList:' + conceptID + '&wt=python')

        return eval(connection.read())['response']['docs'][0]['IX_umlsSemanticType']
    #@timeit
    def filter_concept_with_semantic_type(self):
        """

        :return: filtered concepts for corresponding semantic type
        """
        #start_time = datetime.datetime.now()
        self.filtered_concept= { concepts
                                  for semantic_type in self.selected_semantic_type_list \
                                  if semantic_type in self.semantic_dict \
                         for concepts in self.semantic_dict[semantic_type]}

        #self.filtered_concept = []
        #for semantic_type in self.selected_semantic_type_list:

            #connection = request.urlopen(
                #'http://127.0.0.1:8983/solr/SEMANTIC_CONCEPT/select?indent=on&q=IX_umlsSemanticType:' + semantic_type + '&wt=python')
            #response = eval(connection.read())
            #if len(self.filtered_concept) == 0:
                #self.filtered_concept = response['response']['docs'][0]['IX_umlsConceptList']

            #else:
#            self.filtered_concept.append(concepts for concepts in response['response']['docs'][0]['IX_umlsConceptList'])

        #end_time = datetime.datetime.now()
        #t_delta = end_time - start_time

        #print("PROCESSING TIME for filter_concept_with_semantic_type (sec): {}".format(t_delta.seconds))

    #def get_concept_semantic_type(self):
    #connection = request.urlopen('http://127.0.0.1:8983/solr/MRSTY/select?indent=on&q=IX_umlsCode:' + node + '&wt=python')  # http://127.0.0.1:8983/solr/MRSTY





    def get_cosine_score(self, vec1, vec2):
        """
         returns the normalized cosine similarity between two vector, similar to gensim consine similarity
        """

        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))




