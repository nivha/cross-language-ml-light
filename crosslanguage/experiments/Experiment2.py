# coding=utf-8
import os
import urllib

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
    n_samples_above_beta_one = 12

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

        # load last n_units_per_fold if exists (this is if the experiment failed in the middle...)
        self.last_n_units_per_fold = 1
        self.last_clf_score = None
        self.load_parameters_from_results_file()


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

    def load_parameters_from_results_file(self):
        # if the score files does not yet exists, no n_units_per_fold should be loaded
        if not os.path.exists(self.scores_path): return

        # extract last_n_units_per_fold from the scores file
        with open(self.scores_path) as f:
            s = f.read().strip()
            lines = s.split('\n')

            # if number of lines is greater than self.k_units-1 it means that in the previous run
            # we got to beta larger than one. so we want to extract a few parameters from the previous score file:
            #   last_clf_score - this is the score of the clf for beta=0.9. namely, the highest score the
            #                    clf can get. so we'll be using this one for the rest of the clclf scores for comparison
            if len(lines) >= self.k_units-1:
                last_clf_line = lines[self.k_units-2]
                last_clf_score = last_clf_line.split('\t')[8]
                last_clf_score = float(last_clf_score)
                self.last_clf_score = last_clf_score

            # load last_n_units_per_fold
            last_line = lines[-1]
            n_units_per_fold = last_line.split('\t')[6]
            n_units_per_fold = int(n_units_per_fold)
            # we already have the score for n_units_per_fold, so we now want to start from the next one
            self.last_n_units_per_fold = n_units_per_fold + 1
            print 'loaded last_n_units_per_fold', n_units_per_fold

    def get_articles_from_indices(self, queryset, indices):
        return [queryset[i] for i in indices]

    def add_to_scores_file(self, dst_ds_size, trainset_size, n_units_per_fold, beta, last_clf_score, clclf_score):
        with open(self.scores_path, 'a') as f:
            line = '{:s}\t{:s}\t{:s}\t{:s}\t{:d}\t{:d}\t{:d}\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(
                self.source_categories_names[0], self.source_categories_names[1],
                self.target_categories_names[0], self.target_categories_names[1],
                dst_ds_size, trainset_size, n_units_per_fold, beta, last_clf_score, clclf_score)
            print line
            f.write(line)

    def score_clf(self, clf, fold_generator):
        """
            Advanced Cross-Validation for our needs for a one-language classifier
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

    def score_both_beta_smaller_than_one(self, clf, clclf, init_n_units_per_fold, dst_ds_size):
        for n_units_per_fold in xrange(init_n_units_per_fold, self.k_units):
            fold_generator = FoldGenerator(dst_ds_size, self.k_units, n_units_per_fold)
            beta = fold_generator.beta()
            print 'n_units_per_fold', n_units_per_fold, 'beta:', beta

            # compute scores and write them down
            clf_score = self.score_clf(clf, fold_generator)
            clclf_score = self.score_clclf(clclf, fold_generator)
            self.add_to_scores_file(dst_ds_size, fold_generator.fold_size, n_units_per_fold, beta, clf_score, clclf_score)

        # save last clf score - this is the CVscore of the clf for beta=0.9
        # namely, the best score we can get for one-language learning..
        self.last_clf_score = clf_score
        self.last_n_units_per_fold = self.k_units

    def score_both_beta_larger_than_one_aux(self, dst_ds_size, n_units_per_fold, clclf):
        fold_generator = FoldGenerator(dst_ds_size, self.k_units, n_units_per_fold)
        beta = fold_generator.beta()
        print 'n_units_per_fold', n_units_per_fold, 'beta:', beta

        # compute clclf score and write down
        clclf_score = self.score_clclf(clclf, fold_generator)
        self.add_to_scores_file(dst_ds_size, fold_generator.fold_size, n_units_per_fold, beta, self.last_clf_score, clclf_score)

    def score_both_beta_larger_than_one(self, clclf, dst_ds_size, max_units):

        # calculate the step between each n_units_per_fold.
        # we want to do only self.n_samples_above_beta_one from self.k_units to max_units+1
        step = ((max_units+1) - self.k_units) / self.n_samples_above_beta_one
        print 'continuing till', max_units, 'step', step

        n_units_per_fold = self.last_n_units_per_fold,
        for n_units_per_fold in xrange(self.last_n_units_per_fold, max_units + 1, step):
            self.score_both_beta_larger_than_one_aux(dst_ds_size, n_units_per_fold, clclf)
        # anyway, score the clclf for all the english samples. namely n_units_per_fold=max_units
        if n_units_per_fold < max_units:
            self.score_both_beta_larger_than_one_aux(dst_ds_size, max_units, clclf)

    def score_both(self, clclf, clf):

        dst_ds_size = len(self.target_articles)

        if self.last_n_units_per_fold < self.k_units:
            self.score_both_beta_smaller_than_one(clf, clclf, self.last_n_units_per_fold, dst_ds_size)

        # compute the max_units_per_fold and go on to score clclf
        unit_size = dst_ds_size / self.k_units
        max_units = len(self.source_articles) / unit_size
        self.score_both_beta_larger_than_one(clclf, dst_ds_size, max_units)

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

        self.c_a_title = urllib.unquote(self.c_a.replace('_', r'\ '))
        self.c_b_title = urllib.unquote(self.c_b.replace('_', r'\ '))

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
                enca, encb, esca, escb, dst_ds_size, trainset_size, n_units_per_fold, beta, clf_score, clclf_score = line.split('\t')
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

    # en_cs = ['Marxism', 'Anarchism']
    # es_cs = ['Marxismo', 'Anarquismo']

    en_cs = ['Spirituality', 'Religion']
    es_cs = ['Espiritualidad', urllib.quote('Religión')]

    # en_cs = ['Epistemology', 'Ethics']
    # es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    # en_cs = ['Asian_art', 'Latin_American_art']
    # es_cs = ['Arte_de_Asia', 'Arte_latinoamericano']

    # en_cs = ['Dark_matter', 'Black_holes']
    # es_cs = ['Materia_oscura', 'Agujeros_negros']

    clf1 = SimpleClassifier('es', MultinomialNB(alpha=1e-2, fit_prior=False))
    clclf1 = CrossLanguageClassifier('en', 'es', clf1.clf, Direction.Pre)

    Experiment2Scorer('en', 'es', en_cs, es_cs, [clclf1], [clf1]).score()
    Experiment2Plotter(en_cs, es_cs).plot_scores()
