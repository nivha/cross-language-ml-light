import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'


from clml.models import Category, Article

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

        # Run extraction functions
        self.extract_categories_from_names()
        self.extract_translated_articles()

    def extract_categories_from_names(self):
        self.source_categories = [Category.objects.get(name=name) for name in self.source_categories_names]
        self.target_categories = [Category.objects.get(name=name) for name in self.target_categories_names]

    def extract_translated_articles(self):
        def get_translated(categories_names):
            articles = Article.objects.filter(category__name__in=categories_names)
            translated_ids = [o.id for o in articles if o.has_translations()]
            return articles.filter(id__in=translated_ids)

        self.source_articles = get_translated(self.source_categories_names)
        self.target_articles = get_translated(self.target_categories_names)



if __name__=="__main__":
    en_cs = ['Epistemology', 'Ethics']
    es_cs = ['Epistemolog%C3%ADa', '%C3%89tica']

    q = ArticleExtractor(en_cs, es_cs)
    q.source_articles.count()

    print 123
