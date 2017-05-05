import datetime
from elasticsearch import Elasticsearch, client
from datetime import date, timedelta as td

es = Elasticsearch()  # use default of localhost, port 9200

def user_defined_date_range(d1, d2):
    # User input data range
    delta = d2 - d1

    index_list = []
    for i in range(delta.days + 1):
        date = str(d1 + td(days=i)) + '.json'
        index_list.append(date)

    return index_list


def news_search(index_list, mQuery, catagory):
    data = es.search(index=index_list,
                     body={"query": {"bool": {"should": [{"match": {"body": "{}".format(mQuery)}},
                                                         {"match": {"person": "{}".format(mQuery)}},
                                                         {"match": {"location": "{}".format(mQuery)}},
                                                         {"match": {"organization": "{}".format(mQuery)}},
                                                         {"match": {"primarysection": "{}".format(mQuery)}},
                                                         {"match": {"headline": "{}".format(mQuery)}},
                                                         {"match": {"theme": "{}".format(mQuery)}}]}}},
                     doc_type = catagory)
    return data


def elasearch(index_list):
    query = ""
    while 1:
        mQuery = raw_input("What do you what to ask?\n")
        mQuery = unicode(mQuery, "utf-8")

        #   if user input "exit", stop news recommend
        if mQuery == "exit":
            break

        # determine whether user starts a new query or not
        asking = raw_input("Are you asking a new question?\n")
        asking = unicode(asking, "utf-8")
        if asking in ["yes", "of course", "right", "sure", "correct"]:
            new_query = 1
            query = mQuery
        else:
            new_query = 0
            query += u" "
            query += mQuery

        # start a new query
        if new_query:
            data = news_search(index_list, query, catagory='Sports')
            i = 0
            for rcmd in data['hits']['hits']:
                i += 1
                if i > 3:  # only recommend the first three most revelent news
                    break
            print('\n')

        # user keeps asking relevant query, combine previous query into a new query to do search
        else:
            print("Start News Matching...\n")
            data = news_search(index_list, query, catagory='Sports')
            i = 0
            print("Recommend News Links-->\n")
            for rcmd in data['hits']['hits']:
                i += 1
                if i > 3:  # only recommend the first three most revelent news
                    break


def most_recent_news_recommend():
    today = datetime.date.today()
    yesterday = datetime.date.today() - td(1)
    today = str(today) + '.json'
    yesterday = str(yesterday) + '.json'
    index_list = [today, yesterday]
    elasearch(index_list)


def chosen_date_range_news_recommend(d1, d2):
    index_list = user_defined_date_range(d1, d2)
    elasearch(index_list)


# def hottest_news_recommend():
d1 = date(2017, 3, 18)
d2 = date(2017, 3, 21)
chosen_date_range_news_recommend(d1, d2)
most_recent_news_recommend()