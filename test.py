import cPickle
import os
import collections
from pprint import pprint

def data_stats():
    article_dict = collections.defaultdict(lambda: 0)
    articles = os.listdir("articles/")
    articles.remove(".DS_Store")
    print "Number of articles: {}".format(len(articles))
    for article in articles:
        article_dict[article.split("_")[0]] += 1
    for key in article_dict.keys():
        print "{}: {}".format(key, article_dict[key])

def load_article(fp):
    article = cPickle.load(open(fp,"rb"))
    pprint(vars(article))

if __name__ == '__main__':
    data_stats()
    load_article("articles/Paleontology_5pulv6")
