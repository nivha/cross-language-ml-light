
__author__ = 'Mojo'

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy
from pylab import plot, savefig, clf

class Direction(object):
    Pre = 'pre'
    Post = 'post'


class SimpleClassifierTester(object):
    """
        bla bla..

        training_categories, testing_categories must be at the same length and organised such
        that each train_category are semantically same as the test_category at the same index
        i.e.:
            training_categories = ['Dark_matter', 'Black_holes']
            testing_categories  = ['Materia_oscura', 'Agujeros_negros']
    """

    def __init__(self, source_language, target_language, training_categories, testing_categories,
                 direction):
        self.source_language = source_language
        self.target_language = target_language
        self.training_categories = training_categories
        self.testing_categories = testing_categories
        self.direction = direction

        self.train_data = []
        self.train_target = []
        self.test_data = []
        self.test_target = []

        self._prepare_data()
        self._train()

    def _get_text(self, article):
        if self.direction == Direction.Post:
            return article.articlecontent_set.get(language=self.source_language).text
        if self.direction == Direction.Pre:
            return article.articlecontent_set.get(language=self.target_language).text

    def _prepare_data(self):
        """

        :return:
        """
        # acquire articles data and target for training
        for category in self.training_categories:
            for article in category.article_set.all():
                training_text = self._get_text(article)
                self.train_data.append(training_text)
                self.train_target.append(category.name)

        # acquire articles data and target for testing
        for i, category in enumerate(self.testing_categories):
            for article in category.article_set.all():
                testing_text = self._get_text(article)
                self.test_data.append(testing_text)
                self.test_target.append(self.training_categories[i].name)


    def _train(self):
        """

        :return:
        """
        # self.clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
        #                      ('tfidf', TfidfTransformer()),
        #                      ('clf', SGDClassifier(loss='hinge', penalty='l2',
        #                                            alpha=1e-3, n_iter=5)),
        #                      ])
        self.clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB(alpha=1e-2, fit_prior=False)),
                             ])
        # self.clf = Pipeline([('vect', CountVectorizer(stop_words='english')),
        #                      ('tfidf', TfidfTransformer()),
        #                      ('clf', BernoulliNB(alpha=1.0)),
        #                      ])
        self.clf = self.clf.fit(self.train_data, self.train_target)

    def _test(self):
        predicted = self.clf.predict(self.test_data)
        result = predicted == self.test_target
        score = numpy.mean(result)
        print 'scored:', numpy.sum(result), 'out of:', numpy.size(result)
        return score

    def plot_words_scores(self):
        final_clf = self.clf.steps[2][1]
        classes = final_clf.classes_
        for i, cls_name in enumerate(classes):
            # plot sorted indices
            q = numpy.array(final_clf.feature_log_prob_[i])
            q.sort()
            q = q[::-1]
            clf()
            plot(range(len(q)), q)
            savefig('{:s}.png'.format(cls_name))

    def _k_most_important_words_per_category(self, k):
        countvectorizer = self.clf.steps[0][1]
        final_clf = self.clf.steps[2][1]
        classes = final_clf.classes_
        most_important_words = []
        for i, cls_name in enumerate(classes):
            sorted_indices = final_clf.feature_log_prob_[i].argsort()
            max_indices = sorted_indices[-k:][::-1]
            important_words = [countvectorizer.get_feature_names()[index] for index in max_indices]
            most_important_words.append([cls_name, important_words])

        return most_important_words

    def score(self):
        score = self._test()
        return score



if __name__ == '__main__':
    # en_cs = ['Asian_art', 'Latin_American_art']
    # es_cs = ['Arte_de_Asia', 'Arte_latinoamericano']
    en_cs = ['Black_holes', 'Dark_matter']
    es_cs = ['Agujeros_negros', 'Materia_oscura']
    trainc = map(lambda x: Category.objects.get(name=x), en_cs)
    testc = map(lambda x: Category.objects.get(name=x), es_cs)


    # s = SimpleClassifierTester('en', 'es', trainc, testc, Direction.Pre)
    # s.plot_words_scores()
    # print s.score()
    # s = SimpleClassifierTester('en', 'es', trainc, testc, Direction.Post)
    # print s.score()

    s = SimpleClassifierTester('en', 'es', trainc, testc, Direction.Post)
    for c, l in s._k_most_important_words_per_category(20):
        print c, l