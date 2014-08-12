# coding=utf-8
import os
import urllib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from experiments.utils import ArticleExtractor
from learning.SimpleClassifier import create_simple_classifier

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from clml.models import Category
from learning.CrossLanguageClassifier import CrossLanguageClassifier, Direction

__author__ = 'Ori'




class Experiment1(object):
    """
    Experiment to check which classifier works best for cross-language learning.
    """

    def __init__(self,
                 source_language, target_language,
                 source_categories_names, target_categories_names,
                 classifiers):

        self.source_language = source_language
        self.target_language = target_language

        self.source_categories_names = source_categories_names
        self.target_categories_names = target_categories_names

        extractor = ArticleExtractor(self.source_categories_names, self.target_categories_names)

        self.source_categories = list(extractor.source_categories)
        self.target_categories = list(extractor.target_categories)
        self.source_articles = list(extractor.source_articles)
        self.target_articles = list(extractor.target_articles)

        self.classifiers = classifiers

    def run(self, output_file=None):
        i = 0
        with open(output_file, 'wb') as f:

            s = 'running experiment 1 on categories {:s},{:s}\n'.format(self.source_categories, self.target_categories)
            print s
            f.write(s)

            for classifier in self.classifiers:
                for direction in [Direction.Post, Direction.Pre]:
                    cross_language_classifier = CrossLanguageClassifier(self.source_language,
                                                                        self.target_language,
                                                                        create_simple_classifier(classifier),
                                                                        direction)

                    cross_language_classifier.map_categories(self.source_categories, self.target_categories)

                    # Get a list of all articles from both categories
                    # train_articles = filter(lambda article: article.has_translations(),
                    #                         reduce(lambda a, b: a + b,
                    #                                map(lambda category: list(category.article_set.all()), self.source_categories)))
                    #
                    # test_articles = filter(lambda article: article.has_translations(),
                    #                        reduce(lambda a, b: a + b,
                    #                               map(lambda category: list(category.article_set.all()), self.target_categories)))

                    cross_language_classifier.learn(self.source_articles)
                    score = cross_language_classifier.test(self.target_articles)

                    print i
                    i += 1

                    f.write('score: {:f}, direction: {:s}, classifier: {:s}\n'.format(score, classifier, direction))
                    f.flush()


def run_experiment1(en_cs, es_cs, output_file=None):
    # en_cs = ['Black_holes', 'Dark_matter']
    # es_cs = ['Agujeros_negros', 'Materia_oscura']

    # en_cs = ['Epistemology', 'Ethics']
    # es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    classifiers = [
        SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5),
        SGDClassifier(),
        MultinomialNB(alpha=1e-3, fit_prior=False),
        MultinomialNB(alpha=1e-2, fit_prior=False),
        MultinomialNB(alpha=1e-1, fit_prior=False),
        MultinomialNB(alpha=1, fit_prior=False),
        KNeighborsClassifier(1, weights='uniform'),
        KNeighborsClassifier(3, weights='uniform'),
        KNeighborsClassifier(5, weights='uniform'),
        KNeighborsClassifier(1, weights='distance'),
        KNeighborsClassifier(3, weights='distance'),
        KNeighborsClassifier(5, weights='distance'),
        BernoulliNB(alpha=1.0),
        BernoulliNB(alpha=2.0),
        BernoulliNB(alpha=3.0),
        SVC(),
        SVC(C=1e10),
        # DecisionTreeClassifier(),
    ]

    exp = Experiment1('en', 'es', en_cs, es_cs, classifiers)
    exp.run(output_file)


if __name__ == '__main__':
    # run_experiment1(['Epistemology', 'Ethics'], ['Epistemolog%C3%ADa', '%C3%89tica'], 'score_ethics_epistimology.txt')
    # run_experiment1(['Black_holes', 'Dark_matter'], ['Agujeros_negros', 'Materia_oscura'], 'score_blackholes_darkmatter.txt')
    run_experiment1(['Marxism', 'Anarchism'], ['Marxismo', 'Anarquismo'], 'score_marxism_anarchism.txt')
    # run_experiment1(['Spirituality', 'Religion'], ['Espiritualidad', urllib.quote('Religión')], 'score_religion_spirituality.txt')

    # TODO: automatic output file name and path


