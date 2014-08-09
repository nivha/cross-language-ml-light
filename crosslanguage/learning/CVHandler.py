__author__ = 'Mojo'

from sklearn.cross_validation import KFold


class FoldGenerator(object):

    """
        Gets sizes of english and spanish datasets and return indices of necessary CV stuff..
    """

    def __init__(self, ds_size, k_units, n_units_per_fold, k_folds=10):
        self.ds_size = ds_size
        self.k_units = k_units
        self.n_units_per_fold = n_units_per_fold

        self.unit_size = self.ds_size / self.k_units
        self.fold_size = self.unit_size * self.n_units_per_fold
        self.k_folds = k_folds

    def __iter__(self):
        for fold_i in xrange(self.k_folds):
            first_index = fold_i * self.unit_size
            last_index = min(first_index + self.fold_size, self.ds_size)
            last_train_ids = range(first_index, last_index)
            train_ids = set(last_train_ids + range(self.fold_size - len(last_train_ids)))
            yield train_ids, set(range(self.ds_size)) - train_ids


if __name__ == "__main__":
    f = FoldGenerator(200, 10, 2)
    for i in f:
        print i



