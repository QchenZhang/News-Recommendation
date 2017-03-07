import json
from elasticsearch import Elasticsearch


es = Elasticsearch()  # use default of localhost, port 9200
q = True
with open("./merge.json") as fo:
    doc = json.load(fo)

for art in doc['docs']:
    es.index(index='news', doc_type='article', id=art['id'], body=art)

while q:
    mQuery = raw_input("What do you what to ask?\n")
    print("Finish token :)\n")
    print("Start News Matching...\n")
    mQuery = unicode(mQuery, "utf-8")
    data = es.search(index="news", body={"query": {"bool": {"should": [{"match": {"headline": "{}".format(mQuery)}},
                                                                      {"match": {"theme": "{}".format(mQuery)}}]}}})
    i = 0
    print("Recommend News Links-->\n")
    for rcmd in data['hits']['hits']:
        i += 1
        if i > 3:       #only recommend the first three most revelent news
            break
        print (rcmd['_source']['contenturl'])    #change 'contenturl' to 'body', 'headline', 'theme' and so on
    print('\n')
    if mQuery == "exit":
        q = False
