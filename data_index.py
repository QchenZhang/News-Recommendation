import json
import os
from elasticsearch import Elasticsearch, client

es = Elasticsearch()  # use default of localhost, port 9200
ind = client.IndicesClient(es)


class myindex(object):
    def __init__(self):
        pass

    def indexx(self):
        for filename in os.listdir("news"):    # change news data file path here!
            if filename != '.DS_Store':
                with open("news/{}".format(filename)) as fo:
                    doc = json.load(fo)
                    for art in doc['docs']:
                        if 'primarysection' in art.keys():
                            try:
                                dtype = art['primarysection']
                                dtype = dtype.encode('ascii','ignore')
                                es.index(index='{}'.format(filename), doc_type=dtype, body=art)
                            except ValueError:  # 'primarysection' is blank
                                es.index(index='{}'.format(filename), doc_type='primarysection', body=art)


    def delete_index(self):
        index_list = []
        for filename in os.listdir("../../../news"):
            if filename != '.DS_Store':
                index_list.append(filename)
        es.indices.delete(index=index_list, ignore=[400, 404])  # delete existing index

indexxx = myindex()
indexxx.indexx()  # index data