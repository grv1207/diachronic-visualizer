import redis
import json

"""
time, concept, semnatic

"""
TIME_FRAME = ['1809_1970', '1971_1975', '1976_1980', '1981_1985', '1986_1990', '1991_1995', '1996_2000',
                          '2001_2005','2006_2010', '2011_2012', '2013_2015']


SEMANTIC_TYPE_dict = {'Therapeutic or Preventive Procedure':'tpp',
                      'Finding':'finding',
                      'Clinical Drug':'cd',
                      'Diagnostic Procedure':'dp',
                      'Antibiotic':"antibiotic",
                'Pharmacologic Substance':'ps',
                      'Disease or Syndrome':'ds',
                      'Injury or Poisoning':'ip'
                      ,'Bacterium':'bacterium',
                      'Congenital Abnormality':'ca',
                 'Mental or Behavioral Dysfunction':'mbd',
                      'Sign or Symptom':'ss',
                      'Virus':'virus',
                      'Neoplastic Process':'np'}
from urllib import request


class REDISBACKEND():
    #request_dict = {'concept':_request['concept'], 'semantic_type':_request['semantic_type'], 'topN':_request['neighbor']}
    def __init__(self, request_dict):
        self.r= redis.Redis.from_url('redis://localhost:6379/',db=0) #134.101.0.130
        self.request_dict = request_dict

    #@staticmethod
    def get_concept(self):
        result_time_dict = {}

        for time in TIME_FRAME:
            result_concept = []
            search_concept_list = []
            for semantic in self.request_dict['semantic_type']:
                search_concept_list.append(("{}-{}-{}".format(time,self.request_dict['concept'], SEMANTIC_TYPE_dict[semantic]),semantic))
                #result_concept = [(neighbour_score,semantic) for srch_concept in search_concept_list if self.r.exists(srch_concept) for neighbour_score in json.loads(self.r.get(srch_concept))]\
                #.sort(key= lambda x : x[1],reverse=True)[:self.request_dict['topN']]
            #result_concept = []
            for srch_concept in search_concept_list:
                if self.r.exists(srch_concept[0]):
                    for neighbour, score in json.loads(self.r.get(srch_concept[0])).items():
                        result_concept.append((neighbour, score, srch_concept[1]))

            #result_concept.sort(key=lambda x: x[1], reverse=True)[:self.request_dict['topN']] C1318442
            #if len(result_concept) > self.request_dict['topN']:

            sorted_result_concept_list = sorted(result_concept, key=lambda x: x[1], reverse=True)[:int(self.request_dict['topN'])]
            if sorted_result_concept_list :

                result_time_dict[time] = self.get_topN_neighbour(sorted_result_concept_list)





        return result_time_dict


    def get_topN_neighbour(self, sorted_nieghbour_score_semantic):
        final_neighbor = []
        for neighbor_semantic in sorted_nieghbour_score_semantic:
            _name = self.get_concept_name(neighbor_semantic[0])
            _semantic_type = neighbor_semantic[2]
            concept_id,score = neighbor_semantic[0], neighbor_semantic[1]
            final_neighbor.append(( concept_id,score, _name, _semantic_type))
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





