## Requirements

- Python 2
- Tensorflow > 0.12
- Numpy

News_Crawl.py: Run News_Crawl.py, it will crawl news and comments data from Washington Post starting from date d1 to date d2, combines each news with corresponding comment and then store news with comments on the same date into a single Json file named by the date string, like '2017-5-1.json'. By default, date d1 is the date of today and date d2 is the date of three days ago. User can change date d1 and date d2 to whatever past date that they want. 


data_index.py: Run data_index.py, it will connect to Elasticsearch engine using default of localhost port 9200, and index all news data files in the folder '/news'. Each file storing all news and corresponding comments on a same date in the folder '/news' is named by that date. Indexing will use each file's name as index. 


data_index_delete.py: Run data_index.py, it will connect to Elasticsearch engine using default of localhost port 9200, and delete all existing index.


Elastic_Search.py: Run Elastic_Search.py, it will first take a query sentence as a input, then it will connect to Elasticsearch engine using default of localhost port 9200, and search all indexed news data using BM25 relevance calculation algorithm to calculate the relevance score of each news with the query. After ranking depending on relevance scores, top 5 most relevant news will be returned. 


main.py: Run main.py, it will first take a query sentence as a input, then it will connect to Elasticsearch engine using default of localhost port 9200, and search within indexed dataset, summarizing returned news and re-ranking them. Finally, it will return top 5 most relevant news after re-ranking.
