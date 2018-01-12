# -*- coding: utf-8 -*-
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import gensim
import time

class RemoveTagsPipeline(object):
    # Method which tries to remove HTML tags from text
    def remove_tags(whocares, string):
        string = re.sub('<script[\s\S]+?/script>', '', string)
        string = re.sub('<[^<]+?>', ' ', string)
        return string

    def process_item(self, item, spider):
        if 'title' in item:
            print item.get('title')
            item['title'] = self.remove_tags(item.get('title'))
            item['body'] = self.remove_tags(item.get('body'))
        return item

class TfIdfPipeline(object):
    def process_item(self, item, spider):
        return item

class Word2VecPipeline(object):
    def open_spider(self, spider):
        # Create an empty model
        # Default min_count = 5, so we need to put the same word 5 times to init vocabulary
        w2v = gensim.models.Word2Vec([['seo']], min_count = 1)
        self.name = '/tmp/Word2Vec' + str(time.time())
        # Save it
        w2v.save(self.name)

    def process_item(self, item, spider):
        if 'title' in item:
            # This time, we don't update the item, instead we build the model.
            document = item.get('title') + ' ' + item.get('body')
            words = [[word for word in document.lower().split()]]
            # Load current model
            w2v = gensim.models.Word2Vec.load(self.name)
            # Train our model
            w2v.build_vocab(words, update=True)
            w2v.train(words, total_examples=w2v.corpus_count, epochs=w2v.iter)
            # Save it for the next item
            w2v.save(self.name)
        return item
