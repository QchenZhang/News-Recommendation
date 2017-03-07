import requests
import os, time
import json
from datetime import datetime


def init(cat):
    if not os.path.exists("{}".format(cat)):
        os.makedirs("{}".format(cat))


def get(url):
    r = requests.get(url)
    if 'errorMessage' in r.text:
        raise RuntimeError("RATE exceeds")
    return r.text


def save(dat, filename):
    with open(filename, 'w') as outfile:
        json.dump(dat, outfile, indent=4)


def crawl(cat, year, month, day):
    ################################## PARAMS #################################
    url_template = "https://docs.washpost.com/{}?stdate={}/{}/{}&enddate={}/{}/{}&offset={}&count={" \
                   "}&key=zgi53MiWSM9FbsYAPrvz"

    OFFSET = 0
    COUNT = 100

    ################################## init #################################
    init(cat)

    ################################## crawl #################################
    for i in range(1, 6):
        try:
            dat = get(url_template.format(cat, year, month, day,
                                  year, month, day, OFFSET, COUNT))
            save(dat, "{}.{}.{}.json".format(year, month, day))

        except RuntimeError:
            t = datetime.fromtimestamp(time.time())
            print("{}:{}:{}: RATE LIMIT EXCEEDS".format(t.hour, t.minute, t.second))
            time.sleep(3000)

        OFFSET += COUNT


def add_id(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        num = len(data["docs"])
        for i in range(0,num):
            data["docs"]['id'] = i+1

    os.remove(filename)
# filename = './com/2017.02.17_2017.02.18_100_100.json'


def merge(filename1, filename2):
    with open(filename1) as fo:
        data1 = json.load(fo)

    with open(filename2) as fo:
        data2 = json.load(fo)

    data_news_com = {"docs": []}

    for news in data2['docs']:
        for com in data1['docs']:
            if com['id'] == news['id']:
                assert com['contenturl'] == news['contenturl'], "same id, different url"
                news['comment'] = com['comments']
                data_news_com['docs'].append(news)

    with open("merge.json", 'w') as f:
        json.dump(data_news_com, f, indent=4)


#Let users input start date and end date, the output is merged json file with news and corresponding comments within
# that date range.
if __name__ == "__main__":

    STARTDATE_YEAR  = "2017"
    STARTDATE_MONTH = "03"
    STARTDATE_DAY = "01"

    ENDDATE_YEAR = "2017"
    ENDDATE_MONTH = "03"
    ENDDATE_DAY = "01"

    for year in range(int(STARTDATE_YEAR), int(ENDDATE_YEAR)+1):
        for month in range(int(STARTDATE_MONTH), int(ENDDATE_MONTH)+1):
            for day in range(int(STARTDATE_DAY), int(ENDDATE_DAY)+1):
                for cat in ["docs", "com"]:
                    print ("Crawling {} on {}.{}.{} ...".format(cat, str(year), str(month), str(day)))
                    # crawl(cat, str(year), str(month), str(day))
                    # add_id("{}.{}.{}.json".format(year, month, day))

                # merge("{}/{}.{}.{}.json".format("docs", year, month, day), "{}/{}.{}.{}.json".format("com", year,
                #                                                                                      month, day))
