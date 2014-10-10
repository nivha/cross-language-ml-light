import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'


from clml.models import Category, Article, ArticleContent

__author__ = 'Mojo'


class ArticleExtractor(object):

    def __init__(self, source_categories_names, target_categories_names):
        self.source_categories_names = source_categories_names
        self.target_categories_names = target_categories_names

        # members to be filled automatically by this extractor
        self.source_categories = None
        self.target_categories = None
        self.source_articles = None
        self.target_articles = None
        self.category_map = None

        # Run extraction functions
        self.extract_categories_from_names()
        self.extract_relevant_articles()
        self.map_categories()

    def extract_categories_from_names(self):
        self.source_categories = [Category.objects.get(name=name) for name in self.source_categories_names]
        self.target_categories = [Category.objects.get(name=name) for name in self.target_categories_names]

    def extract_relevant_articles(self):
        """
        Retrives only articles which:
        1. Have translation
        2. Do not intersect between the two categories
        """

        def get_translated(article_set):
            return [o for o in article_set if o.has_translations()]

        def get_non_intersecting_articles(categories):
            """ clean articles in the intersection """
            c1_articles = Article.objects.filter(category=categories[0])
            c2_articles = Article.objects.filter(category=categories[1])

            c1_urls = set([o.url for o in c1_articles])
            c2_urls = set([o.url for o in c2_articles])
            intersecting_urls = c1_urls.intersection(c2_urls)
            # remove articles from intersection
            intersecting_ids = []
            for url in intersecting_urls:
                ass = Article.objects.filter(category__in=categories, url=url)
                intersecting_ids.extend([o.id for o in ass])

            return Article.objects.filter(category__in=categories).exclude(id__in=intersecting_ids)

        # remove articles in intersection
        self.source_articles = get_non_intersecting_articles(self.source_categories)
        self.target_articles = get_non_intersecting_articles(self.target_categories)

        # get only translated
        self.source_articles = get_translated(self.source_articles)
        self.target_articles = get_translated(self.target_articles)

    def map_categories(self):
        """
        Create a mapper from target categories to source categories.
        """
        source_categories_names = [category.name for category in self.source_categories]
        target_categories_names = [category.name for category in self.target_categories]

        self.category_map = dict(zip(target_categories_names, source_categories_names))


if __name__ == "__main__":
    en_cs = ['Epistemology', 'Ethics']
    es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    q = ArticleExtractor(en_cs, es_cs)
    #
    # for a in q.source_articles:
    #     a.articlecontent_set.get(language='es')
    #     if a.articlecontent_set.count()!=2:
    #         print a
    #
    # print "AAAAAAAAAAAAAAAA"
    #
    # for a in q.target_articles:
    #     a.articlecontent_set.get(language='es')
    #     if a.articlecontent_set.count()!=2:
    #         print a
