import json
from urllib import response
import inflect
from flask import Flask,render_template
import random
from flask import request
from urllib import request as rs

#from  DB_connection import DatabaseConnection as dc
from pytable_DB import PY_table_connection as py_table
import datetime
from proof_concept import pairwise_similarity as pw
import template_generation as tg
from redis_backend import REDISBACKEND as rb



app = Flask(__name__)

@app.route("/basic", methods=['GET','POST'])
def post_function():
    if request.method == 'GET':

        return render_template('basic.html')
    if request.method == 'POST':
        _request =  request.get_json(force=True)
        start_time = datetime.datetime.now()
        result = ''
        if _request['request_type']=='top_neighbor':
            #dc(_request['concept'],_request['semantic_type']).get_nearest_neighbour()
            result = tg.generate_template_neighbor(py_table(_request['concept'],_request['semantic_type'],_request['neighbor']).get_nearest_neighbour(),
                                       _request['neighbor'])
        elif  _request['request_type']=='poc':
            # dictionary for each concept
            selected_poc = _request['concept']
            result= tg.generate_template_POC(tg.P_O_C[selected_poc])

        elif _request['request_type']=='cosine_similarity':
            concept_1 = _request['concept1']
            concept_2 = _request['concept2']
            #{"request_type" : "cosine_similarity", "concept1" : conceptID_1, "concept2" : conceptID_2}
            result = tg.generate_template_pairWiseScore(concept_1,concept_2,pw(concept_1,concept_2).get_SGNS_score())


        elif _request['request_type']=='top_neighbor_redis':
            request_dict = {'concept':_request['concept'], 'semantic_type':_request['semantic_type'], 'topN':_request['neighbor']}
            result = tg.generate_template_neighbor(rb(request_dict).get_concept(),_request['neighbor'])

        #print(result)
        end_time =   datetime.datetime.now()
        t_delta = end_time - start_time

        print("PROCESSING TIME(sec): {}".format(t_delta.seconds))
        #_dict = {1:d1,2:d2,3:d3} #
        #print(_dict)


        return json.dumps(result)

@app.route("/proxysolr", methods=['GET','POST'])
def get_solr_data():
    if request.method == 'POST':
        _request = request.get_json(force=True)
        print(_request)
        table, query = _request['table'],_request['query']
        #query = '\ '.join(map(str, query.strip().split(' ')))
        query_string =  "http://127.0.0.1:8983/solr/"+table+"/select?indent=on&q=IX_generalText:\""+ query.replace(" ","%20")+"\"&wt=json"

        connection = rs.urlopen(query_string)
        result = eval(connection.read()) #['response'] #['docs'][0]['IX_umlsName'] IX_generalText
        return json.dumps(result)
        #return "http://127.0.0.1:8983/solr/"+table+"/select?indent=on&q=IX_umlsName:" + query+"&wt=json"


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
