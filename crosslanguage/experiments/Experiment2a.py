
import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

import random
from sklearn.naive_bayes import MultinomialNB
from clml.models import Article
from experiments.utils import ArticleExtractor
from learning.CVHandler import FoldGenerator
from learning.CrossLanguageClassifier import CrossLanguageClassifier, Direction
from learning.SimpleClassifier import create_simple_classifier, SimpleClassifier
import numpy as np
import ujson

from crosslanguage.settings import RESULTS_DIR


__author__ = 'Mojo'


class Experiment2Scorer(object):
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

        # define paths for scores and shuffled_ids
        c_a = self.source_categories_names[0]
        c_b = self.source_categories_names[1]
        self.shuffled_ids_path = os.path.join('shuffled', 'exp2_shuffled_ids_{:s}_{:s}.txt'.format(c_a, c_b))
        self.scores_path = os.path.join(RESULTS_DIR, 'experiment2', 'scores_{:s}_{:s}.txt'.format(c_a, c_b))

        # extract categories from categories_names
        extractor = ArticleExtractor(self.source_categories_names, self.target_categories_names)
        self.source_articles = list(extractor.source_articles)
        self.target_articles = list(extractor.target_articles)
        # shuffle the articles for the learning to be homogeneous..
        self.shuffle_articles_if_needed()
        # only take part of the articles
        self.target_articles = self.target_articles[:self.max_dst_articles]

        # initiate clclfs category map
        for clclf in self.clclfs:
            clclf.category_map = extractor.category_map


    def shuffle_articles_if_needed(self):

        if os.path.exists(self.shuffled_ids_path):
            self.load_shuffled()
            return

        random.shuffle(self.source_articles)
        random.shuffle(self.target_articles)

        # save shuffled ids to file in case experiment fails..
        source_ids = [o.id for o in self.source_articles]
        target_ids = [o.id for o in self.target_articles]

        d = {
            'source_ids': source_ids,
            'target_ids': target_ids,
        }
        jd = ujson.dumps(d)
        with open(self.shuffled_ids_path, 'w') as f:
            f.write(jd)

    def load_shuffled(self):
        print 'loading shuffled...'
        with open(self.shuffled_ids_path) as f:
            s = f.read()
            d = ujson.loads(s)

            source_ids = d['source_ids']
            target_ids = d['target_ids']


            self.source_articles = [Article.objects.get(id=i) for i in source_ids]
            self.target_articles = [Article.objects.get(id=i) for i in target_ids]

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
        for train, test in fold_generator:
            trainset = self.get_articles_from_indices(self.target_articles, train)
            testset = self.get_articles_from_indices(self.target_articles, test)

            clf.learn(trainset)
            score = clf.test(testset)
            scores.append(score)

        return np.average(scores)


    def score_clclf(self, clclf, fold_generator):
        fold_generator.set_custom_ds_size(len(self.source_articles))
        testset = self.target_articles

        scores = []
        for train, test in fold_generator:
            trainset = self.get_articles_from_indices(self.source_articles, train)

            clclf.learn(trainset)
            score = clclf.test(testset)
            scores.append(score)

        return np.average(scores)

    def score_both(self, clclf, clf):

        dst_ds_size = len(self.target_articles)
        unit_size = dst_ds_size / self.k_units
        max_units = len(self.source_articles) / unit_size

        beta_scores = []
        last_clf_score = None
        for n_units_per_fold in xrange(1, self.k_units):

            fold_generator = FoldGenerator(dst_ds_size, self.k_units, n_units_per_fold)
            beta = fold_generator.beta()
            print 'beta:', beta

            clf_score = self.score_clf(clf, fold_generator)
            last_clf_score = clf_score
            print clf_score

            clclf_score = self.score_clclf(clclf, fold_generator)
            self.add_to_scores_file(dst_ds_size, fold_generator.fold_size, beta, last_clf_score, clclf_score)

            #beta_scores.append( ( beta, (clf_score, clclf_score) ) )

        print 'continuing till', max_units
        for n_units_per_fold in xrange(self.k_units, max_units + 1):
            fold_generator = FoldGenerator(dst_ds_size, self.k_units, n_units_per_fold)
            beta = fold_generator.beta()
            print 'n_units_per_fold', n_units_per_fold, 'beta:', beta

            clclf_score = self.score_clclf(clclf, fold_generator)
            self.add_to_scores_file(dst_ds_size, fold_generator.fold_size, beta, last_clf_score, clclf_score)

    def add_to_scores_file(self, dst_ds_size, trainset_size, beta, last_clf_score, clclf_score):
        with open(self.scores_path, 'a') as f:
            line = '{:s}\t{:s}\t{:s}\t{:s}\t{:d}\t{:d}\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(
                self.source_categories_names[0], self.source_categories_names[1],
                self.target_categories_names[0], self.target_categories_names[1],
                dst_ds_size, trainset_size, beta, last_clf_score, clclf_score)
            print line
            f.write(line)


    def score(self):
        for i in xrange(len(self.clclfs)):
            clclf = self.clclfs[i]
            clf = self.clfs[i]
            self.score_both(clclf, clf)


class Experiment2Plotter(object):

    def __init__(self, source_categories_names, target_categories_names):

        # self.source_language = source_language
        # self.target_language = target_language
        self.source_categories_names = source_categories_names
        self.target_categories_names = target_categories_names

        self.c_a = self.source_categories_names[0]
        self.c_b = self.source_categories_names[1]
        self.shuffled_ids_path = os.path.join('shuffled', 'exp2_shuffled_ids_{:s}_{:s}.txt'.format(self.c_a, self.c_b))
        self.scores_path = os.path.join(RESULTS_DIR, 'experiment2', 'scores_{:s}_{:s}.txt'.format(self.c_a, self.c_b))
        self.figpath = os.path.join(RESULTS_DIR, 'experiment2', 'scores_{:s}_{:s}.png'.format(self.c_a, self.c_b))

        self.c_a_title = self.c_a.replace('_', r'\ ')
        self.c_b_title = self.c_b.replace('_', r'\ ')

    def plot_scores(self):
        import pylab

        with open(self.scores_path) as f:
            s = f.read().strip()
            lines = s.split('\n')

            betas = []
            clf_scores = []
            clclf_scores = []
            trainset_sizes = []
            for line in lines:
                enca, encb, esca, escb, dst_ds_size, trainset_size, beta, clf_score, clclf_score = line.split('\t')
                betas.append(beta)
                clf_scores.append(clf_score)
                clclf_scores.append(clclf_score)
                trainset_sizes.append(trainset_size)

            # pylab.xkcd()
            pylab.plot(betas, clf_scores, label="$One\ Language\ Spanish\ Classifier$")
            pylab.plot(betas, clclf_scores, label="$Cross-Language\ Classifier$")
            pylab.ylabel(r"$CV\ Score$")
            pylab.xlabel(r"$\beta\ Score$")
            # title = r"$Comparison\ between\ one-language\ Spanish\ classifier\ (10-fold CV)\ to cross-language\ classifier$"
            # title += "\n"
            title = r"$Categories:\ {:s}\ vs.\ {:s}$".format(self.c_a_title, self.c_b_title)
            pylab.title(title)
            pylab.legend()
            pylab.savefig(self.figpath)


if __name__ == "__main__":

    print "HELLO"

    # en_cs = ['Epistemology', 'Ethics']
    # es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    en_cs = ['Asian_art', 'Latin_American_art']
    es_cs = ['Arte_de_Asia', 'Arte_latinoamericano']

    # en_cs = ['Dark_matter', 'Black_holes']
    # es_cs = ['Materia_oscura', 'Agujeros_negros']

    clf = SimpleClassifier('es', MultinomialNB(alpha=1e-2, fit_prior=False))
    clclf = CrossLanguageClassifier('en', 'es', clf.clf, Direction.Pre)

    # Experiment2Scorer('en', 'es', en_cs, es_cs, [clclf], [clf]).score()
    Experiment2Plotter(en_cs, es_cs).plot_scores()
