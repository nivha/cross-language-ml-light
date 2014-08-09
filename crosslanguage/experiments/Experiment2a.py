from learning.CVHandler import FoldGenerator

__author__ = 'Mojo'


en_cs = ['Epistemology', 'Ethics']
es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']


class Experiment2(object):
    """

    """

    def _init_(self,
               source_language, target_language,
               source_categories_names, target_categories_names,
               classifiers):

        self.source_language = source_language
        self.target_language = target_language
        self.source_categories_names = source_categories_names
        self.target_categories_names = target_categories_names
        self.classifiers = classifiers

    def create_graph(self, k_units):
        # decide number of units
        for units_num_per_fold in xrange(k_units):
            fold_generator = FoldGenerator()

