from IPython.nbformat.v2.nbxml import _get_text
import numpy

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

        assert (self.source_language == article.original_language)  # TODO remove...

        if self.direction == Direction.Post:
            return article.articlecontent_set.get(language=self.source_language).text
        if self.direction == Direction.Pre:
            return article.articlecontent_set.get(language=self.target_language).text

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
        self.category_map = dict(zip(target_categories, source_categories))

    def predict(self, test_data):
        """
        Predicts the category of a given list of texts
        :param test_data: The texts to predict
        :return:
        """
        return self.simple_classifier.predict(test_data)

    def test(self, test_articles):
        """

        :param test_articles: A list of articles to test
        :return:
        """
        if self.map_categories() is None:
            raise LearnerException('Map categories missing')

        test_data = [self._get_text(article) for article in test_articles]
        test_target = [self.category_map[article.category.name] for article in test_articles]

        predicted = self.simple_classifier.predict(test_data)
        result = predicted == self.test_target
        score = numpy.mean(result)
        print 'scored:', numpy.sum(result), 'out of:', numpy.size(result)
        return score


if __name__ == '__main__':
    





