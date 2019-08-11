import time

from tables import *
import numpy as np
import pickle
import datetime
from operator import itemgetter
from urllib import request
#TOPN=3
#from multiprocess import Process, Manager
#with open('data_dir_UI/semantic_conceptList.bin','rb') as fin:   #semantic_cui_name_dict
    #SEMANTIC_DICT = pickle.load(fin)

TIME_FRAME = ['1809_1970', '1971_1975', '1976_1980', '1981_1985', '1986_1990', '1991_1995', '1996_2000',
                          '2001_2005','2006_2010', '2011_2012', '2013_2015']


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
        #self.neg_top_neighbour = -(self.top_neighbour+1)
        self.selected_semantic_type_list= selected_semantic_type_list        
        self.COSINE_SCORE_ = open_file("/Users/gauravvashisth/Documents/UNI-Folder/thesis/model_vec/cosine_score_DB.h5", mode="r", title="cosine_simialrity DB")
      
    #@timeit

    def get_negihbor_at_each_period(self):
        score_time_dict = {}
        for time in TIME_FRAME:
            score_list= []
            for semantic in self.selected_semantic_type_list:
                #table_at_concept = EMBEDDINGFILE.get_node('/embedding_group/{}'.format(time)) 
                if self.COSINE_SCORE_.__contains__('/cosine_group/{}/{}'.format(time,self.conceptID)) :
                    table_node = self.COSINE_SCORE_.get_node('/cosine_group/{}/{}/{}'.format(time,self.concept_ID,semantic)) 
                # what if conceptID not exist!!..??
                    score_list.append(table_node.read())

            score_time_dict[time] = self.get_topN_neighbour(score_list.sort(key= lambda x : x[1])[:self.top_neighbour])

        self.COSINE_SCORE_.close()
        return score_time_dict


    def get_topN_neighbour(self, sorted_list):
        final_neighbor = []
        #start_time = datetime.datetime.now()
        for neighbor in sorted_list:
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
   




