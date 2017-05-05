import datetime
from elasticsearch import Elasticsearch, client
from datetime import date, timedelta as td


es = Elasticsearch()  # use default of localhost, port 9200
d1 = date(2017, 4, 23)
d2 = date(2017, 4, 25)
# d2= datetime.date.today()
# d1= datetime.date.today() - td(2)


class Elastic(object):
    def __init__(self):
        self.mQuery = ''

    def search(self, Query):
        # today = datetime.date.today()
        # yesterday = datetime.date.today() - td(1)
        # today = str(today) + '.json'
        # yesterday = str(yesterday) + '.json'
        # index_list = [today, yesterday]


        delta = d2 - d1
        index_list = []
        for i in range(delta.days + 1):
            date = str(d1 + td(days=i)) + '.json'
            index_list.append(date)


        # self.mQuery = raw_input("What do you what to ask?\n")
        self.mQuery = Query
        self.mQuery = unicode(self.mQuery, "utf-8")

      # if user input "exit", stop news retrieval and recommend
      #   if mQuery == "exit":
      #       break
      #
      # else, keep doing news retrieval and recommend
      #   print("Finish token :)\n")
      #   print("Start News Matching...\n")
        data = es.search(index=index_list,
                         body={"query": {"bool":{"should": [{"match": {"body": "{}".format(self.mQuery)}},
                                                             {"match": {"person": "{}".format(self.mQuery)}},
                                                             {"match": {"location": "{}".format(self.mQuery)}},
                                                             {"match": {"organization": "{}".format(self.mQuery)}},
                                                             {"match": {"primarysection": "{}".format(self.mQuery)}},
                                                             {"match": {"headline": "{}".format(self.mQuery)}},
                                                             {"match": {"theme": "{}".format(self.mQuery)}}]}}},
                         size = 5)   # doc_type=category,

#        R = []
#        Body = []
        result = {'headline+blurb': "", 'body': ""}
        for rcmd in data['hits']['hits']:
            print rcmd['_source']['contenturl']
            result1 = rcmd['_source']['headline'].encode('ascii', 'ignore')
            result2 = rcmd['_source']['blurb'].encode('ascii', 'ignore')
            result3 = rcmd['_source']['body'].encode('ascii','ignore')
            result['headline+blurb'] += result1 + " " + result2
            result['body'] += result3
#            Body.append(result)
#            result = result.split()
#            R.append(result[0:50])


        return result, self.mQuery
## result['headline+blurb'] = headline + blurb
## result['body'] = body


mysearch = Elastic()
Output, myQuery = mysearch.search(Query='Seattle')