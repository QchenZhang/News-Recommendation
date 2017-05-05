import requests
import json
import os
import time
import datetime
from jsonmerge import Merger
from datetime import date, timedelta as td
from termcolor import colored


d2= datetime.date.today()
d1= datetime.date.today() - td(2)
# d1 = date(2017, 4, 23)    # input start date
# d2 = date(2017, 4, 25)    # input end date


schema = {
    "properties": {
        "docs": {
            "mergeStrategy": "append"
        }
    }
}
merger = Merger(schema)

if not os.path.exists("news"):
    os.makedirs("news")

delta = d2 - d1


def get(url):
    r = requests.get(url)
    if '"docs": []' in r.text:
        return None
    if 'errorMessage' in r.text:
        print(r.text)
        raise RuntimeError("RATE exceeds")
    return r.text

for i in range(delta.days + 1):
    date1 = str(d1 + td(days=i)).replace("-", "/")
    date2 = str(d1 + td(days=i+1)).replace("-", "/")
    result_docs = {}
    result_comments = {}
    offset = 0

    for j in range(5):
        date1 = date1.replace("-", "/")

        News_API = "https://docs.washpost.com/docs?stdate=" + date1 + "&enddate=" + date2 + "&offset=" + str(offset) +\
                    "&count=100" + "&key=zgi53MiWSM9FbsYAPrvz"
        Comment_API = "https://docs.washpost.com/comments?stdate=" + date1 + "&enddate=" + date2 + \
                      "&offset=" + str(offset) + "&count=100" + "&key=zgi53MiWSM9FbsYAPrvz"

        date1 = date1.replace("/", "-")

        try:
            docs = get(News_API)
            print colored(date1, 'green')
            if docs:
                with open("temp.json", 'w') as tmp:
                    tmp.write(docs)
                with open("temp.json") as tmp:
                    docs = json.load(tmp)
                result_docs = merger.merge(result_docs, docs)
            else:
                print ("Finished crawling docs on {}".format(date1))

            comments = get(Comment_API)
            print colored(date1, 'red')
            if comments:
                with open("temp.json", 'w') as tmp:
                    tmp.write(comments)
                with open("temp.json") as tmp:
                    comments = json.load(tmp)
                result_comments = merger.merge(result_comments, comments)
            else:
                print ("Finished crawling comments on {}".format(date1))
                break

        except RuntimeError:
            print("RATE LIMIT EXCEEDS")
            time.sleep(900)

        offset += 100

    data_news_com = {"docs": []}

    for news in result_docs['docs']:
        for com in result_comments['docs']:
            if com['contenturl'] == news['contenturl']:
                news['comment'] = com['comments']
                data_news_com['docs'].append(news)

    with open("news/{}.json".format(date1), 'w') as f:
        json.dump(data_news_com, f, indent=4)
