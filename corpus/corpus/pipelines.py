# -*- coding: utf-8 -*-
import gensim
from gensim.parsing.porter import PorterStemmer
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import time
from w3lib.html import remove_tags, remove_tags_with_content

class RemoveTagsPipeline(object):
    # Method which tries to remove HTML tags from text
    def remove_tags(whocares, string):
        string = remove_tags_with_content(string, which_ones=('style', 'script'))
        string = remove_tags(string)
        return string

    def process_item(self, item, spider):
        if 'title' in item:
            item['title'] = self.remove_tags(item.get('title'))
            item['body'] = self.remove_tags(item.get('body'))
        return item

class TfIdfPipeline(object):
    def process_item(self, item, spider):
        return item

class Word2VecPipeline(object):
    def open_spider(self, spider):
        # Create an empty model
        w2v = gensim.models.Word2Vec([['seo']], min_count = 1)
        self.name = '/tmp/Word2Vec' + str(time.time())
        # Save it
        w2v.save(self.name)
        self.p = PorterStemmer()
        self.stop_words = set(stopwords.words('french'))

    def process_item(self, item, spider):
        if 'title' in item:
            # This time, we don't update the item, instead we build the model.
            document = item.get('title') + ' ' + item.get('body')
            words = [word_tokenize(self.p.stem_sentence(s)) for s in sent_tokenize(document)]
            # Load current model
            w2v = gensim.models.Word2Vec.load(self.name)
            # Train our model
            w2v.build_vocab(words, update=True)
            w2v.train(words, total_examples=w2v.corpus_count, epochs=w2v.iter)
            # Save it for the next item
            w2v.save(self.name)
        return item
