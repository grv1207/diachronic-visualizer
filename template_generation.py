import json
from urllib import response
import inflect
from flask import Flask,render_template
import random
from flask import request
from urllib import request as rs
"""P_O_C = {
'prolactinoma': {'prolactinoma microadenoma ': {'C0405509': ['0', '0', 0.66262275, 0.54440689, 0.44922948, 0.37779367, 0.34743065, 0.29177722, 0.18979838, 0.19755921, 0.21123663], 'C0107994': ['0', '0', '0', '0', 0.55305272, 0.48342836, 0.52728522, 0.55635273, 0.59360123, 0.60409808, 0.52539885], 'C2985562': ['0', '0', 0.48753753, 0.59765482, 0.57160139, 0.52410096, 0.55390811, 0.53110683, 0.44768715, 0.5545224, 0.48804265], 'C0178601': ['0', '0', 0.33194765, 0.43894148, 0.44228685, 0.43444353, 0.45228657, 0.52720654, 0.53966844, 0.54997325, 0.51071352], 'C0006230': ['0', '0', 0.45131585, 0.62103021, 0.62598133, 0.59428096, 0.53627586, 0.56609428, 0.48793998, 0.45009214, 0.42320225]}},
'wbc': {'myelosis; chronic ': {'C1268567': ['0', '0', '0', '0', 0.2490271, 0.26454526, 0.27102599, 0.47468138, 0.52885199, 0.59806621, 0.55641145], 'C0026236': [0.52554119, 0.52803147, 0.47169521, 0.4242419, 0.4019413, 0.4074077, 0.405422, 0.35637814, 0.33318093, 0.2758168, 0.24311979], 'C0149417': ['0', 0.538118, 0.47837371, 0.37362707, 0.33686733, 0.29819643, 0.28916529, 0.23821554, 0.17015362, 0.1222654, 0.083602719], 'C0935989': ['0', '0', '0', '0', '0', '0', '0', 0.70910513, 0.71445668, 0.71932453, 0.65033937], 'C1522691': [0.54799104, 0.46896988, 0.42788428, 0.36631066, 0.3789528, 0.36808977, 0.31156904, 0.20778099, 0.15459271, 0.16467637, 0.18855499], 'C0700014': [0.60368747, 0.53620487, 0.4753648, 0.39876193, 0.3835215, 0.4071539, 0.35125861, 0.33958906, 0.29615659, 0.25048888, 0.17078567], 'C0722911': [0.550529, 0.44404197, 0.44304287, 0.32813025, 0.3140285, 0.33117265, 0.27314842, 0.25426444, 0.21394242, 0.18578488, 0.12671052]}},
'hc': {'post-transfusion hepatitis non A non B virus ': {'C0035525': ['0', '0', 0.28134534, 0.23280458, 0.30224097, 0.584589, 0.56895411, 0.58721334, 0.59545022, 0.5944882, 0.62625921], 'C1738934': ['0', '0', '0', '0', '0', '0', '0', '0', 0.46153748, 0.5396148, 0.58453262], 'C0391001': ['0', '0', '0', '0', '0', '0', 0.45999175, 0.46697062, 0.50699019, 0.5285151, 0.54447556], 'C3252090': ['0', '0', '0', '0', '0', '0', '0', '0', '0', 0.60077584, 0.57885695], 'C1876229': ['0', '0', '0', '0', '0', '0', '0', '0', 0.48669642, 0.53149533, 0.61241853], 'C0796545': ['0', '0', '0', '0', '0', '0', 0.35579389, 0.45141876, 0.45973986, 0.47428259, 0.48206383]}},
'cc':{'warts virus ': {'C1721787': ['0', '0', '0', '0', '0', '0', '0', '0', 0.57702756, 0.59562504, 0.59982079],
                       'C0282515': [0.35970959, 0.26942953, 0.16002257, 0.19706772, 0.17417565, 0.20351374, 0.21107316, 0.23535602, 0.2277824, 0.25306761, 0.23399273]}},
'ulcer':{'ulcer; peptic ': {'C0749751': [0.55211413, 0.58360577, 0.61329138, 0.63890249, 0.67187989, 0.6233719, 0.58960253, 0.60492146, 0.55049562, 0.42622021, 0.4086448], 'C0559761': ['0', '0', '0', '0', '0', 0.59486508, 0.65070719, 0.60067511, 0.60460734, 0.52956897, 0.49516869], 'C0161899': [0.43357077, 0.45572835, 0.49277258, 0.53837633, 0.46015334, 0.45694256, 0.40277594, 0.40603802, 0.41622031, 0.39395308, 0.41160893], 'C0017118': [0.55055439, 0.54396075, 0.60450995, 0.58712029, 0.57524276, 0.53298301, 0.52974904, 0.49992272, 0.44756299, 0.43156031, 0.42150745], 'C0581065': ['0', '0', '0', '0', '0', 0.58075309, 0.55469376, 0.5638442, 0.50911283, 0.44830972, 0.4357993]}},
'minoxidil':{'minoxidil products ': {'C0497248': ['0', '0', 0.58019686, 0.50441891, 0.38241014, 0.21518654, 0.26149544, 0.25464588, 0.32386887, 0.24395745, 0.22912088], 'C0155583': ['0', 0.55869424, 0.54726976, 0.37425435, 0.22760338, 0.20014575, 0.197466, 0.19487824, 0.21253818, 0.15041217, 0.16417846], 'C0162311': ['0', 0.25387079, 0.21881166, 0.35749587, 0.4280591, 0.34518832, 0.35313481, 0.44745007, 0.45617181, 0.42331254, 0.41962972], 'C0597853': ['0', 0.60363781, 0.51741403, 0.46346462, 0.30765122, 0.29849231, 0.31225717, 0.26170743, 0.27845168, 0.18867755, 0.18906507], 'C0574769': ['0', 0.29740536, 0.21969175, 0.44370446, 0.44101149, 0.39515463, 0.39835459, 0.40693188, 0.36508334, 0.36584118, 0.39573863], 'C0263477': ['0', '0', '0', '0', 0.34378332, 0.4658646, 0.40284902, 0.47733486, 0.3877492, 0.47048917, 0.40250832]}}

} """

P_O_C = {'prolactinoma': {'prolactinoma microadenoma ': {'C0405509': ['0', '0', 0.66262275, 0.54440689, 0.44922948, 0.37779367, 0.34743065, 0.29177722, 0.18979838, 0.19755921, 0.21123663], 'C0107994': ['0', '0', '0', '0', 0.55305272, 0.48342836, 0.52728522, 0.55635273, 0.59360123, 0.60409808, 0.52539885], 'C2985562': ['0', '0', 0.48753753, 0.59765482, 0.57160139, 0.52410096, 0.55390811, 0.53110683, 0.44768715, 0.5545224, 0.48804265],'C0006230': ['0', '0', 0.45131585, 0.62103021, 0.62598133, 0.59428096, 0.53627586, 0.56609428, 0.48793998, 0.45009214, 0.42320225]}},
'wbc': {'myelosis; chronic ': {'C1268567': ['0', '0', '0', '0', 0.2490271, 0.26454526, 0.27102599, 0.47468138, 0.52885199, 0.59806621, 0.55641145], 'C0026236': [0.52554119, 0.52803147, 0.47169521, 0.4242419, 0.4019413, 0.4074077, 0.405422, 0.35637814, 0.33318093, 0.2758168, 0.24311979], 'C0935989': ['0', '0', '0', '0', '0', '0', '0', 0.70910513, 0.71445668, 0.71932453, 0.65033937],'C0700014': [0.60368747, 0.53620487, 0.4753648, 0.39876193, 0.3835215, 0.4071539, 0.35125861, 0.33958906, 0.29615659, 0.25048888, 0.17078567]}},
'hc': {'post-transfusion hepatitis non A non B virus ': {'C0035525': ['0', '0', 0.28134534, 0.23280458, 0.30224097, 0.584589, 0.56895411, 0.58721334, 0.59545022, 0.5944882, 0.62625921], 'C0391001': ['0', '0', '0', '0', '0', '0', 0.45999175, 0.46697062, 0.50699019, 0.5285151, 0.54447556], 'C1876229': ['0', '0', '0', '0', '0', '0', '0', '0', 0.48669642, 0.53149533, 0.61241853], 'C0796545': ['0', '0', '0', '0', '0', '0', 0.35579389, 0.45141876, 0.45973986, 0.47428259, 0.48206383]}},
'cc':{'warts virus ': {'C1721787': ['0', '0', '0', '0', '0', '0', '0', '0', 0.57702756, 0.59562504, 0.59982079],'C0013216': [0.167288,0.122594,0.077773,0.0776243,0.0918741,0.121828	,0.159229,0.200169,0.163206,0.137768,0.206424], 'C1522449' : [0.171578,0.240223,0.169031,0.176738,0.198358,0.212661,0.196066,0.212169,0.212469,0.236057,0.272367]}},
'ulcer':{'ulcer; peptic ': {'C0749751': [0.55211413, 0.58360577, 0.61329138, 0.63890249, 0.67187989, 0.6233719, 0.58960253, 0.60492146, 0.55049562, 0.42622021, 0.4086448], 'C0559761': ['0', '0', '0', '0', '0', 0.59486508, 0.65070719, 0.60067511, 0.60460734, 0.52956897, 0.49516869], 'C0017118': [0.55055439, 0.54396075, 0.60450995, 0.58712029, 0.57524276, 0.53298301, 0.52974904, 0.49992272, 0.44756299, 0.43156031, 0.42150745], 'C0581065': ['0', '0', '0', '0', '0', 0.58075309, 0.55469376, 0.5638442, 0.50911283, 0.44830972, 0.4357993]}},
'minoxidil':{'minoxidil products ': {'C0155583': ['0', 0.55869424, 0.54726976, 0.37425435, 0.22760338, 0.20014575, 0.197466, 0.19487824, 0.21253818, 0.15041217, 0.16417846], 'C0162311': ['0', 0.25387079, 0.21881166, 0.35749587, 0.4280591, 0.34518832, 0.35313481, 0.44745007, 0.45617181, 0.42331254, 0.41962972], 'C0597853': ['0', 0.60363781, 0.51741403, 0.46346462, 0.30765122, 0.29849231, 0.31225717, 0.26170743, 0.27845168, 0.18867755, 0.18906507], 'C0574769': ['0', 0.29740536, 0.21969175, 0.44370446, 0.44101149, 0.39515463, 0.39835459, 0.40693188, 0.36508334, 0.36584118, 0.39573863]}}

         }


COLOR_LIST = ["#E74C3C","#AF7AC5","#2980B9","#85C1E9","#48C9B0","#52BE80","#F4D03F","#E67E22","#E59866","#5D6D7E"]
TIME_FRAME = ['1809_1970', '1971_1975', '1976_1980', '1981_1985', '1986_1990', '1991_1995', '1996_2000','2001_2005','2006_2010','2011_2012','2013_2015']
p = inflect.engine()


class Data_template_neighbour:
    def __init__(self,chartTitle,label,cui_period_dict,cui_name_period_dict,cui_semantic_period_dict,backgroundColor,borderColor,data_list,showLine=False,lineTension=0):
     self.chartTitle = chartTitle
     self.label= label
     self.cui_period_dict = cui_period_dict
     self.cui_name_period_dict= cui_name_period_dict
     self.cui_semantic_period_dict= cui_semantic_period_dict
     self.backgroundColor= backgroundColor
     self.borderColor= borderColor
     self.data= data_list
     self.fill= False
     self.showLine= showLine
     self.lineTension = lineTension


    def to_json(self):
        return {"chartTitle": self.chartTitle,"label":self.label,'cui':self.cui_period_dict,'backgroundColor':self.backgroundColor,'borderColor':self.borderColor,
                'cui_name' : self.cui_name_period_dict,'cui_semantic': self.cui_semantic_period_dict, 'data':self.data,'fill':self.fill,'showLine':self.showLine,'lineTension':self.lineTension}


def get_concept_name( conceptID):
    #connection = rs.urlopen('http://127.0.0.1:8983/solr/MRCONSO/select?indent=on&q=IX_umlsCode:' + conceptID + '&wt=python')
    connection = rs.urlopen(
        'http://127.0.0.1:8983/solr/MRCONSO_substring/select?indent=on&q=IX_umlsCode:' + conceptID + '&wt=python')
    return eval(connection.read())['response']['docs'][0]['IX_generalText']


def get_semantic_type(conceptID):
    connection = rs.urlopen(
            'http://127.0.0.1:8983/solr/SEMANTIC_TYPE/select?indent=on&q=IX_umlsConceptList:' + conceptID + '&wt=python')

    return eval(connection.read())['response']['docs'][0]['IX_umlsSemanticType']



def generate_template_neighbor(data_dictionary, top_neighbour):
    main_json = {}
    top_neighbour = int(top_neighbour)
    neighbor_set= {i: "{} Neighbor".format(p.ordinal(i+1)) for i in range(top_neighbour)} #= {0:'First Neighbor',1:'Second Neighbor',2:'Third Neighbor'}
    random_color = random.sample(COLOR_LIST,top_neighbour)
    for neighbour in range(top_neighbour):
        cui, cui_name, semantic_type, data_list = {}, {},{}, []
        for time in TIME_FRAME:
            time_t=time
            if time_t in data_dictionary:
                if data_dictionary[time_t]:
                    if len(data_dictionary[time_t]) > neighbour:
                        neighbour_score = data_dictionary[time_t][neighbour]
                        cui[time],cui_name[time],semantic_type[time] = neighbour_score[0],neighbour_score[2],neighbour_score[3]
                        data_list.append(neighbour_score[1])
                else:
                    cui[time], cui_name[time],semantic_type[time] = '', '',''
                    data_list.append('n')
            else:
                cui[time], cui_name[time], semantic_type[time] = '', '', ''
                data_list.append('n')

        main_json[neighbour] = Data_template_neighbour(chartTitle="TOP {} Neighbors".format(top_neighbour),label=neighbor_set[neighbour],cui_period_dict=cui,cui_name_period_dict=cui_name,
                                                       backgroundColor=random_color[neighbour],borderColor=random_color[neighbour],
                                                       data_list=data_list,cui_semantic_period_dict=semantic_type).to_json()

    return main_json







def generate_template_POC(data_dictionary):
    main_json = {}
    for actual_name in data_dictionary:
        drug_dictionary = data_dictionary[actual_name]
        random_color = random.sample(COLOR_LIST, len(drug_dictionary.values()))
        for i,drug in enumerate(drug_dictionary):
            cui, cui_name, semantic_type, data_list = {}, {}, {}, drug_dictionary[drug]
            name , semantic_name = get_concept_name(drug), get_semantic_type(drug)
            for time in TIME_FRAME:
                cui[time], cui_name[time], semantic_type[time] = drug , name , semantic_name #CONCEPT_DICT[drug][0],CONCEPT_DICT[drug][1] CONCEPT_DICT[drug][0]


            main_json[i]= Data_template_neighbour(chartTitle=actual_name.upper(),label=name,cui_period_dict=cui,cui_name_period_dict=cui_name,
                                                           backgroundColor=random_color[i],borderColor=random_color[i],
                                                           data_list=data_list,cui_semantic_period_dict=semantic_type,showLine=True,lineTension=0).to_json()
    return main_json


def generate_template_pairWiseScore(concept1,concept2,data_list):
    main_json = {}
    random_color = random.sample(COLOR_LIST, 1)
    cui, cui_name, semantic_type, data_list = {}, {}, {}, data_list
    actual_name =  get_concept_name(concept1) #CONCEPT_DICT[concept1][0].upper()
    name, semantic_name = get_concept_name(concept2), get_semantic_type(concept2)
    for time in TIME_FRAME:
        cui[time], cui_name[time], semantic_type[time] = concept2 ,name, semantic_name #CONCEPT_DICT[concept2][0],CONCEPT_DICT[concept2][1] CONCEPT_DICT[concept2][0]


    main_json[0]= Data_template_neighbour(chartTitle=actual_name.upper(),label=name,cui_period_dict=cui,cui_name_period_dict=cui_name,
                                                   backgroundColor=random_color[0],borderColor=random_color[0],
                                                   data_list=data_list,cui_semantic_period_dict=semantic_type,showLine=True,lineTension=0).to_json()
    return main_json


