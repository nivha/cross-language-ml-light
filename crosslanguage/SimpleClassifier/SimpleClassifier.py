import os

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from clml.models import Category

__author__ = 'Ori'


def create_simple_classifier(classifier_type):
    return Pipeline([('vect', CountVectorizer(stop_words='english')),
                     ('tfidf', TfidfTransformer()),
                     ('clf', classifier_type),
                     ])

# class SimpleClassifier(object):
#     """
#     Gets a classifier type and a marked list of articles (learning set).
#     Returns a one-language classifier.
#     """
#
#     def __init__(self, classifier_type):
#
#
#     def fit(self, train_data, train_target):
#         """
#         Train the classifier on a given data
#         :return:
#         """
#         self.clf = self.clf.fit(train_data, train_target)
#
#     def predict(self, data_to_predict):
#         return self.clf.predict(data_to_predict)
#
#     def transform(self, data_to_transform):
#         return self.clf.transform(data_to_transform)


if __name__ == '__main__':
    en_cs = ['Black_holes', 'Dark_matter']
    trainc = map(lambda x: Category.objects.get(name=x), en_cs)

    # Built total train data and target lists
    data = []
    target = []
    for category in trainc:
        for article in category.article_set.all():
            training_text = article.get_original_content().text
            data.append(training_text)
            target.append(category.name)

    clf = create_simple_classifier(MultinomialNB(alpha=1e-2, fit_prior=False))

    scores = cross_validation.cross_val_score(clf, data, target, cv=30)

    print scores
    print sum(scores)*1.0 / len(scores)


