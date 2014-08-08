import os
import random
import numpy

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


class SimpleClassifier(object):
    """
    Gets a classifier type and a marked list of articles (learning set).
    Returns a one-language classifier.
    """

    def __init__(self, language, classifier_type):
        self.language = language
        self.clf = create_simple_classifier(classifier_type)

    def learn(self, source_articles):
        """
        Train the classifier on a given data
        :return:
        """
        train_data = [article.articlecontent_set.get(language=self.language).text for article in source_articles]
        train_target = [article.category.name for article in source_articles]

        self.clf = self.clf.fit(train_data, train_target)

    def test(self, test_articles):
        test_data = [article.articlecontent_set.get(language=self.language).text for article in test_articles]
        test_target = [article.category.name for article in test_articles]

        predicted = self.clf.predict(test_data)
        result = predicted == test_target
        score = numpy.mean(result)
        print 'scored:', numpy.sum(result), 'out of:', numpy.size(result)
        return score


if __name__ == '__main__':
    # cs = ['Black_holes', 'Dark_matter']
    cs = ['Epistemolog%C3%ADa_old', '%C3%89tica_old']  # ['Epistemology', 'Ethics']
    trainc = map(lambda x: Category.objects.get(name=x), cs)

    # Built total train data and target lists
    data = []
    target = []
    all_articles = []
    # for category in trainc:
    #     for article in category.article_set.all():
    #         training_text = article.get_original_content().text
    #         data.append(training_text)
    #         target.append(category.name)

    all_articles = reduce(lambda a, b: a + b,
                          map(lambda category: list(category.article_set.all()), trainc))
    random.shuffle(all_articles)

    simple_classifier = SimpleClassifier('es', MultinomialNB(alpha=1e-2, fit_prior=False))

    foldsize = len(all_articles) / 5
    learn_articles = all_articles[:4*foldsize]
    test_articles = all_articles[4*foldsize:]

    simple_classifier.learn(learn_articles)

    print simple_classifier.test(test_articles)

    # clf = simple_classifier.clf
    # scores = cross_validation.cross_val_score(clf, data, target, cv=10)
    # print scores
    # print sum(scores)*1.0 / len(scores)


