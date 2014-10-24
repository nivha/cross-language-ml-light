import os
from sklearn.naive_bayes import MultinomialNB
from SimpleClassifier import create_simple_classifier

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

import numpy
from clml.models import Category, ArticleContent

__author__ = 'Ori'


class Direction(object):
    Pre = 'pre'
    Post = 'post'


class LearnerException(Exception):
    pass


class CrossLanguageClassifier(object):
    """
    Cross language classifier.
    Learns on articles of language A, classifies articles of language B.
    """

    def __init__(self, source_language, target_language, simple_classifier, direction):

        self.source_language = source_language
        self.target_language = target_language

        self.simple_classifier = simple_classifier

        self.direction = direction
        self.train_data = []
        self.train_target = []

        self.category_map = None

    def _get_text(self, article):
        try:
            if self.direction == Direction.Post:
                return article.articlecontent_set.get(language=self.source_language).text
            if self.direction == Direction.Pre:
                    return article.articlecontent_set.get(language=self.target_language).text
        except ArticleContent.DoesNotExist:
            import traceback
            print traceback.format_exc()
            print ">>>", article.id
            print article
            raise Exception()

    def learn(self, source_articles):
        """
        Learns from the source django-articles
        :param source_articles: list of articles to learn from
        """

        # Build the data and labels
        self.train_data = [self._get_text(article) for article in source_articles]
        self.train_target = [article.category.name for article in source_articles]

        self.simple_classifier.fit(self.train_data, self.train_target)

    def map_categories(self, source_categories, target_categories):
        """
        Create a mapper from target categories to source categories.
        :param source_categories: A list of the source language categories
        :param target_categories: A list of target language categories which fit to the source
            categirues by the index
        """
        source_categories_names = [category.name for category in source_categories]
        target_categories_names = [category.name for category in target_categories]

        self.category_map = dict(zip(target_categories_names, source_categories_names))

    def test(self, test_articles):
        """
        Tests the classifier on a given test set, and returns its score.
        :param test_articles: A list of articles to test
        :return:
        """
        if self.category_map is None:
            raise LearnerException('Map categories missing')

        test_data = [self._get_text(article) for article in test_articles]
        test_target = [self.category_map[article.category.name] for article in test_articles]

        predicted = self.simple_classifier.predict(test_data)
        result = predicted == test_target
        score = numpy.mean(result)
        # print 'scored:', numpy.sum(result), 'out of:', numpy.size(result)
        return score


if __name__ == '__main__':
    # en_cs = ['Black_holes', 'Dark_matter']
    # es_cs = ['Agujeros_negros', 'Materia_oscura']

    # en_cs = ['Asian_art', 'Latin_American_art']
    # es_cs = ['Arte_de_Asia', 'Arte_latinoamericano']

    en_cs = ['Epistemology', 'Ethics']
    es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    trainc = map(lambda x: Category.objects.get(name=x), en_cs)
    testc = map(lambda x: Category.objects.get(name=x), es_cs)

    # Built total train data and target lists
    # train_articles = []
    # test_articles = []
    #
    # for category in trainc:
    #     for article in category.article_set.all():
    #         if article.has_translations():
    #             train_articles.append(article)
    #
    # for category in testc:
    #     for article in category.article_set.all():
    #         if article.has_translations():
    #             test_articles.append(article)

    train_articles = filter(lambda article: article.has_translations(),
                            reduce(lambda a, b: a + b,
                                   map(lambda category: list(category.article_set.all()), trainc)))

    test_articles = filter(lambda article: article.has_translations(),
                           reduce(lambda a, b: a + b,
                                  map(lambda category: list(category.article_set.all()), testc)))

    clclf = CrossLanguageClassifier('en',
                                    'es',
                                    create_simple_classifier(MultinomialNB(alpha=1e-3, fit_prior=False)),
                                    Direction.Post)

    clclf.learn(train_articles)
    clclf.map_categories(trainc, testc)
    score = clclf.test(test_articles)

    print 'score:', score





