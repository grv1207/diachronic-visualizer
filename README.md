# diachronic-visualizer


This reposiroty contains source for **diachronic-visualizer** used to visualize the embedding for experiments from **Exploring Diachronic Changes of Biomedical Knowledge using Distributed Concept Representations** (https://www.aclweb.org/anthology/W19-5037)

## Components of diachronic-visualizer
* DB_connection.py contains utility function to connect with MYSQL database, provided embedding are stored in a database "DB_embedding" and tables(13 time frames) containing embedding (AVOID THIS METHOD, as it is super slow)
* backend_python.py is middleware between database and the frontend of this application. This file is the main file which we run to start the application.
* embedding_pytable.py contains source for interacting pytable database, provided the database cosine_score_DB.h5 exists which is the cosine similarity between a concept against other concept for each time.
* proof_concept.py contains embedding for all the 6 proof of concept used for this study. Database used here is embedding_index_DB.h5
* pytable_DB.py  contains source for interacting pytable database.  Database used here is embedding_index_DB.h5. If we use pytable_DB.py than we dont have use embedding_pytable.py
* redis_backend.py used for "TOP-N neighbour" feature, where cosine between concept is calculated for each concept.
* template_generation.py used for generating JSON string against user query result.

### Before running diachronic Visualizer, we need to configure some database
* create a database for embedding table and store them in pyttables, embedding can be obtained from https://www.aclweb.org/anthology/W19-5037
* Store Concept name and Semantic types in SOLR database
* Addtionally we have used REDIS DB to store cosine similarity for faster access to "TOP-N neighbour feature". However, in theory we can work with Pyttables given we can compromise with the retrieval time 

**To run diachronic Visualizer**
* `run python backend_python.py`
