from __future__ import division
import tensorflow as tf
import numpy as np
import time
import Helper
from qa_cnn import InsQACNN
import operator
from Elastic_Search import Elastic
from embedding import Word2Vec
import json
from elasticsearch import Elasticsearch
from termcolor import colored

class NewsRetrieval:

    def __init__(self):

          self.batch_size = 100
          self.l2_reg_lambda = 0
          self.Embeding_len = 50
          self.num_filters = 500
          self.filter_sizes = "1,2,3,5"
          self.embedding_dim = 300
          self.allow_soft_placement = True
          self.log_device_placement = False
          session_conf = tf.ConfigProto(
              allow_soft_placement=self.allow_soft_placement,
              log_device_placement=self.log_device_placement)
          self.sessnews = tf.Session(config=session_conf)
          #self.sessnews.run(tf.global_variables_initializer())
          self.cnn = InsQACNN(
                    sequence_length=self.Embeding_len,
                    batch_size=self.batch_size,
                    embedding_size=self.embedding_dim,
                    filter_sizes=list(map(int, self.filter_sizes.split(","))),
                    num_filters=self.num_filters,
                    l2_reg_lambda=self.l2_reg_lambda)

          self.savernews = tf.train.Saver(tf.global_variables())
         # self.savernews.restore(self.sessnews, "./restore/20000model")



    def Ranking(self, sentence):

        en = Elastic()
        Answers, Context, query = en.search(sentence)    # Returned parameters have been changed, only two parameters
        #  are returned, please change correspondingly

        if Answers == "":
            Result = {}
            Result['blurb+headline'] = None
            Result['body'] = None
            return Result

        else:
            Question = en.mQuery
            Databas_Tot = list()

            if len(Answers) == 5:
                    for i in range(5):
                        Database = list()
                        Data_ques = list()
                        Data_ans = list()
                        Database.append('1')
                        Database.append('quas:' + str(1))

                        Ans = ' '.join(word for word in Answers[i])

                        items = Question.strip().split(' ')
                        for j in range(len(items)):
                            Data_ques.append((items[j]) + '_')
                        for j in range(self.Embeding_len - len(items)):
                            Data_ques.append('<a>_')

                        res1 = "".join(Data_ques)
                        Database.append(res1)

                        items = Ans.strip().split(' ')
                        for j in range(len(items)):
                            Data_ans.append((items[j]) + '_')
                        for j in range(self.Embeding_len - len(items)):
                            Data_ans.append('<a>_')

                        res2 = "".join(Data_ans)
                        Database.append(res2)

                        Databas1 = list()
                        for k, item in enumerate(Database):
                            Databas1.append(item)
                            Databas1.append(' ')

                        res_new = "".join(Databas1)
                        Databas_Tot.append(res_new)

                    vocab = set()
                    for line in Databas_Tot:
                        items = line.strip().split(' ')
                        for i in range(2, 4):
                            words = items[i].split('_')
                            vocab.update(words)
                    W = Word2Vec('GoogleNews-vectors-negative300.bin', vocab)

                    with tf.Graph().as_default():
                      with tf.device("/cpu:1"):

                        with self.sessnews.as_default():
                            #ranking = self.Ranking_Step(self.sess, self.cnn, Databas_Tot, W, self.batch_size)
                            #print ranking
                            ranking = [0,1,2,3,4]
                            Best_ans = Context[ranking[0]]
                            Best_ans = Best_ans.split(' ')[0:100]
                            Best_ans = ' '.join(word for word in Best_ans)
                            Answers = ' '.join(word for word in Answers[ranking[0]])
                            Result = {}
                            Result['blurb+headline'] = Answers
                            Result['body'] = Context[ranking[0]]
            else:

                Result = {}
                Result['blurb+headline'] = Answers[0]
                Result['body'] = Context[0]


        return Result

    def Ranking_Step(self, sess, cnn, Databas_Tot, W, batch_size):

        scoreList = []

        x_test_1, x_test_2, x_test_3 = Helper.load_data_val_6(Databas_Tot, W, batch_size)
        feed_dict = {
            cnn.input_x_1: x_test_1,
            cnn.input_x_2: x_test_2,
            cnn.input_x_3: x_test_3,
            cnn.dropout_keep_prob: 1.0
        }
        batch_scores = sess.run([cnn.cos_12], feed_dict)
        for score in batch_scores[0]:
            scoreList.append(score)

        sessdict = {}
        index = int(0)
        for line in (Databas_Tot):
            items = line.strip().split(' ')
            qid = items[1].split(':')[1]
            if not qid in sessdict:
                sessdict[qid] = []
            sessdict[qid].append((scoreList[index], items[0]))
            index += 1
            if index >= len(Databas_Tot):
                break

        for k, v in sessdict.items():
            Res = sorted(range(len(v)), key=v.__getitem__,reverse=True)


        return Res


T = NewsRetrieval()