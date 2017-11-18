import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.model_selection import train_test_split
import cPickle
from sklearn.model_selection import GridSearchCV

X = []
Y = []
#Import articles
for f in os.listdir("articles/"):
    if f[0] != "." and f!="rename.sh":
        f = "articles/"+f
        article = cPickle.load(open(f,"rb"))
        X.append(article.article_text)
        Y.append(article.link_flair_text)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=42)
print "Train Size:%d\nTest Size:%d" % (len(Y_train),len(Y_test))


params = {'C': [0.1, 1, 10, 100, 1000], 'gamma': [0.1, 0.01, 0.001, 0.0001], 'kernel': ['rbf','linear']}
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     #('clf', GridSearchCV(SVC(),params)),])
                     ('clf', GradientBoostingClassifier()),])
text_clf.fit(X_train,Y_train)
print "Models Trained"
predicted = text_clf.predict(X_test)


from sklearn import metrics
print(metrics.classification_report(Y_test, predicted))
