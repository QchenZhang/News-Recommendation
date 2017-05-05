#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import os,sys
import time
import datetime
import data_helpers
from text_cnn import TextCNN
from tensorflow.contrib import learn
import csv
from nltk import tokenize

tf.flags.DEFINE_integer("batch_size", 100, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "runs/1489183683/checkpoints", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", True, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
# Parameters
# ==================================================
# Eval Parameters
class Summarization(object):

    def __init__(self):
        self.translator = Translator()
    def getSummary(self,query,docs):
        buf_outcome = []
        x = self.translator.getlist(query,docs)
        for x_sub in x:
            if FLAGS.eval_train:
                x_raw = x_sub
                y_test = None
            else:
                x_raw = ["a masterpiece four years in the making", "everything is off."]
                y_test = None
            # Map data into vocabulary
            vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
            vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
            #print x_raw
            x_test = np.array(list(vocab_processor.transform(x_raw)))

            # Evaluation
            # ==================================================
            # checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
            # checkpoint_file = 'news_recommend/runs/1489183683/checkpoints/model-30000'
            graph = tf.Graph()
            with graph.as_default():
                session_conf = tf.ConfigProto(
                  allow_soft_placement=FLAGS.allow_soft_placement,
                  log_device_placement=FLAGS.log_device_placement)
                sess = tf.Session(config=session_conf)
                with sess.as_default():
                    # Load the saved meta graph and restore variables
                    # saver = tf.train.import_meta_graph("../{}.meta".format(checkpoint_file))
                    # saver.restore(sess, checkpoint_file)
                    saver = tf.train.import_meta_graph('runs/1489183683/checkpoints/model-30000.meta')
                    saver.restore(sess, 'runs/1489183683/checkpoints/model-30000')

                    # Get the placeholders from the graph by name
                    input_x = graph.get_operation_by_name("input_x").outputs[0]
                    # input_y = graph.get_operation_by_name("input_y").outputs[0]
                    dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

                    # Tensors we want to evaluate
                    predictions = graph.get_operation_by_name("output/predictions").outputs[0]

                    # Generate batches for one epoch
                    batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)
                    #batches = test_data.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

                    # Collect the predictions here
                    all_predictions = []

                    for x_test_batch in batches:
                        batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                        all_predictions = np.concatenate([all_predictions, batch_predictions])

            # Print accuracy if y_test is defined
            if y_test is not None:
                correct_predictions = float(sum(all_predictions == y_test))
            # Save the evaluation
            outcome_buf =np.column_stack((np.array(x_raw), all_predictions))
            buf = []
            for element in outcome_buf:
                if element[1]=='1.0':
                    buf.append(element[0])
            buf_outcome.append(max(buf, key=len))


        return buf_outcome
        # Ali ask for list outcome from summerization


class Translator(object):
    reload(sys)
    sys.setdefaultencoding('utf8')
    def __init__(self):
        pass

    def getlist(self,query,docs):
        # docs =[]
        # docs.append(
        #     "Dear Readers: Happy new year, and I wish you and yours (pets included) a good year! It's a good day to relax and take some time off, or clean out a kitchen drawer! There is something rewarding about getting just one messy drawer in order. I'm going to be working on a few kitchen drawers. Here is how I do it: I spread out a stack of newspapers, or put an old sheet on the floor. While watching TV, I go through the stuff and separate, keep, give away or toss. How many knives and spoons do I really need in the utensils drawer? Not six of each kind! P.S.: How does all of that stuff end up in there? Dear Heloise: It used to be hard to keep up with receipts during a business trip or on vacation until I learned this hint: When I check into my hotel, they give me the room key in a small, credit-card-size envelope. I place the key in my wallet and store the receipts in the envelope. J.M., via email J.M.: Good hint. I use a hotel envelope, write the city and travel dates on the outside and fill it with receipts. Dear Heloise: I sew and use a variety of textiles. Remembering how to clean and maintain the fabric was hard until a friend and fellow sewer gave me this hint: When she decides on the material, she takes a picture of the top of the bolt, which has the specifics on the fabric. When the project is completed, she downloads and makes a copy of the information and the finished project, and files it away for future reference. Frances in Austin, Tex. Dear Heloise: I cook with wooden utensils. Over time, I have noticed that some are stained with age and use. I know I'll probably have to replace those, but is there a way to revive them? A.H. in Louisiana A.H. in Louisiana: Of course there is! 1. Scrub them with a drop of dish soap and a hefty dose of salt, which acts like a scrubbing compound. Rinse well and dry. This may be enough to \"bring them back to life.\" 2. You can use a mild bleach-and-water solution -- say, 1 tablespoon to a quart of water. Or, pour 3 percent hydrogen peroxide over the spoons and let them soak for 20-30 minutes. 3. Re-season by coating with mineral oil, letting them soak overnight, then wiping them off with a paper towel. 4. Don't put them in the dishwasher, don't soak them too long in water, and always wash right away. P.S.: Treat yourself to some new ones! Dear Heloise: As the toothpaste tube gets smaller, I roll it up and use a metal clip to keep it from rolling out again. The clips are the ones you use to clamp multiple sheets of paper. They work like a gem. Timothy T. in Harrisburg, Pa. Heloise's column appears six days a week at www.washingtonpost.com/advice. Send a hint to Heloise, P.O. Box 795000, San Antonio, Tex. 78279-5000, or e-mail it to Heloise@Heloise.com. 2016, King Features Syndicate")
        # docs.append(
        #     "We at KidsPost like to start off the new year with a new calendar, especially one featuring baby animal photos. But store-bought calendars have a serious flaw: not enough holidays. Usually, only two or three are highlighted for each month. There are many more reasons to celebrate. So we put out our own calendar, one that features lesser-known, odd or downright silly holidays. Feel free to print it out for 12 more reasons to have fun or have a laugh in 2016. Opposite Day (January 25): We're not sure we can trust our sources on this one. If it really is Opposite Day, wouldn't they insist it was Normal Day or Just What You Would Expect Day? International Pancake Day (February 9): Nearly everyone flips for flapjacks hot off the griddle. Get up a little early and make some. Awkward Moments Day (March 18): Everyone has done something embarrassing. Today's the day to roll with it and have a laugh. National Look Alike Day (April 20): Do teachers always confuse you with one of your friends? Coordinate your outfits today for added fun. Lost Sock Memorial Day (May 9): If your drawer is half-filled with single socks, this is the day to say goodbye to them. Blame the dryer, and move on. International Mud Day (June 29): This is official permission to play in the mud. Seriously! I Forgot Day (July 2): If you don't write this one down, well, you might forget it. Middle Child Day (August 12): They may not be first in their families, but they've been part of a lot of first families. Fifty-two percent of presidents were middle children. Ask a Stupid Question Day (September 30): People say, \"there's no such thing as a stupid question.\" If you don't believe that, have no fear about asking anything today. World Smile Day (October 2): Harvey Ball, the creator of the familiar smiley face, started this day in 1999 to remind people to smile and to do something to make someone else smile. World Toilet Day (November 19): Mom and Dad might talk to you about bathroom humor if you mention this holiday, but it wasn't invented to gross out anyone. The United Nations created this day to remind the world that 2.4 billion people don't have access to a toilet. Monkey Day (December 14): Learn something about these adorable and highly intelligent primates. Or you could use this day to act like a monkey - but we must warn you that, even on this day, jumping on the bed is a risky business.")

        answer = []
        for doc in docs:
            list = tokenize.sent_tokenize(doc)
            paragraph = []
            temp_b =[]
            for l in list:
                # print l
                paragraph.append(query + " ?\t" + l + " .\n")
            answer.append(paragraph)
        return answer



# tf.flags.DEFINE_integer("batch_size", 1000, "Batch Size (default: 64)")
# tf.flags.DEFINE_string("checkpoint_dir", "runs/1489183683/checkpoints", "Checkpoint directory from training run")
# tf.flags.DEFINE_boolean("eval_train", True, "Evaluate on all training data")
#
# # Misc Parameters
# tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
# tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
#
# FLAGS = tf.flags.FLAGS
# FLAGS._parse_flags()
# summarization = Summarization()
# summarization.getSummary()
