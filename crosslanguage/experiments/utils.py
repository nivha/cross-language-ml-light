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
        self.extract_translated_articles()
        self.map_categories()

    def extract_categories_from_names(self):
        self.source_categories = [Category.objects.get(name=name) for name in self.source_categories_names]
        self.target_categories = [Category.objects.get(name=name) for name in self.target_categories_names]

    def extract_translated_articles(self):
        def get_translated(categories):
            articles = Article.objects.filter(category__in=categories)
            translated_ids = [o.id for o in articles if o.has_translations()]
            return articles.filter(id__in=translated_ids)

        self.source_articles = get_translated(self.source_categories)
        self.target_articles = get_translated(self.target_categories)

    def map_categories(self):
        """
        Create a mapper from target categories to source categories.
        """
        source_categories_names = [category.name for category in self.source_categories]
        target_categories_names = [category.name for category in self.target_categories]

        self.category_map = dict(zip(target_categories_names, source_categories_names))



if __name__=="__main__":
    en_cs = ['Epistemology', 'Ethics']
    es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    # q = ArticleExtractor(en_cs, es_cs)
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

    print 123

    ArticleContent.DoesNotExist