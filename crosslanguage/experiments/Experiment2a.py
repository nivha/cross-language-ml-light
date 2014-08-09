from sklearn.naive_bayes import MultinomialNB
from experiments.utils import ArticleExtractor
from learning.CVHandler import FoldGenerator
from learning.CrossLanguageClassifier import CrossLanguageClassifier, Direction
from learning.SimpleClassifier import create_simple_classifier, SimpleClassifier
import numpy as np

__author__ = 'Mojo'


class Experiment2a(object):
    """

    """
    k_units = 10
    max_dst_articles = 200

    def __init__(self,
                source_language, target_language,
                source_categories_names, target_categories_names,
                clclfs, clfs):
        """

        :param source_language:
        :param target_language:
        :param source_categories_names:
        :param target_categories_names:
        :param clclfs: the  best clclfs from experiment1 that we want to check now
        :param clfs: the respective clfs for each clclfs (so we can test it as one-language-clf)

        """

        self.source_language = source_language
        self.target_language = target_language
        self.source_categories_names = source_categories_names
        self.target_categories_names = target_categories_names
        self.clclfs = clclfs
        self.clfs = clfs

        # extract categories from categories_names
        extractor = ArticleExtractor(self.source_categories_names, self.target_categories_names)
        self.source_articles = list(extractor.source_articles)
        self.target_articles = list(extractor.target_articles[:self.max_dst_articles])

        # shuffle the articles for the learning to be homogeneous..

    def get_articles_from_indices(self, queryset, indices):
        return [queryset[i] for i in indices]

    def score_clf(self, clf, fold_generator):
        """
            Advanced Cros-Validation for our needs for a one-language classifier
        :param clf:
        :param fold_generator:
        :return:
        """

        scores = []
        i = 0
        for train, test in fold_generator:
            print i
            i += 1
            trainset = self.get_articles_from_indices(self.target_articles, train)
            testset = self.get_articles_from_indices(self.target_articles, test)

            clf.learn(trainset)
            score = clf.test(testset)
            scores.append(score)

        print scores
        return np.average(scores)


    def score_clclf(self, clclf, train, test):
        pass


    def score_clclf_clf(self, clclf, clf):

        src_ds_size = len(self.source_articles)
        dst_ds_size = len(self.target_articles)

        beta_scores = []
        for n_units_per_fold in xrange(1, self.k_units):

            fold_generator = FoldGenerator(dst_ds_size, self.k_units, n_units_per_fold)
            beta = fold_generator.beta()
            print beta

            clf_score = self.score_clf(clf, fold_generator)
            print clf_score

            # clclf_score = self.score_clclf(clclf, train, test)
            # beta_scores.append( ( beta, (clf_score, clclf_score) ) )

    def score(self):
        for i in xrange(len(self.clclfs)):
            clclf = self.clclfs[i]
            clf = self.clfs[i]
            self.score_clclf_clf(clclf, clf)

if __name__ == "__main__":

    en_cs = ['Epistemology', 'Ethics']
    es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']


    clf = SimpleClassifier('es', MultinomialNB(alpha=1e-2, fit_prior=False))
    clclf = CrossLanguageClassifier('en', 'es', clf, Direction.Pre)

    Experiment2a('en', 'es', en_cs, es_cs, [clclf], [clf]).score()
