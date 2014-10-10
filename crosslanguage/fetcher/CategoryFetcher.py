# coding=utf-8
import random
import urllib

__author__ = 'Niv & Ori'

from wikitools import wiki
from wikitools import category
from fetcher.utils import cat_lang


class CategoryFetcher(object):
    """
        :params
        @param language - relevant language of given wiki

        Code example:

            cf = CategoryFetcher('es')
            articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
            for article in articles:
                print article

    """

    def __init__(self, language='en'):
        self.language = language

        # base_sites_by_language = {
        #     'en':   "https://en.wikipedia.org/w/api.php",
        #     'es':   "http://es.wikipedia.org/w/api.php"
        # }
        self.site_url = "https://{:s}.wikipedia.org/w/api.php".format(language)
        self.site = wiki.Wiki(self.site_url)


    def get_category_articles(self, category):
        return [article for article in category.getAllMembersGen()]

    def is_category(self, category):
        category_pattern = u'{:s}:'.format(cat_lang[self.language])
        return category[:len(category_pattern)] == category_pattern

    def attach_metadata(self, article):
        """ attaches the original url as an attribute """
        article.url = u"http://{:s}.wikipedia.org/wiki/".format(self.language) + article.urltitle
        return article

    def get_category_recursively(self, category_title, max_articles_num=None, max_depth=None,
                                 max_articles_per_subcategory=None):
        """
        Iterative BFS on the category tree
        returns all articles found in the run, as wiki Page objects

        :param category_title: title of needed category
        :param max_articles_num: maximum number of articles to fetch. stops after reaching the limit
                                 'None' means without limit.
        :param max_depth: max depth to iterate on (in categories depth)
        :param max_articles_per_subcategory: max number of article to take from each subcategory
        :return:
        """

        closed_categories = set()
        open_categories = [(category_title, 0)]  # (category-title, depth)
        articles = set()
        depth_categories = {0: [category_title]}
        current_max_depth = 0

        def pop_category():
            for depth in range(current_max_depth+1):
                if depth in depth_categories and depth_categories[depth]:
                    category = depth_categories[depth].pop(random.randrange(len(depth_categories[depth])))
                    if len(depth_categories[depth])==0: pass
                    return category, depth
            return None, None

        def push_category(category, depth):
            if depth in depth_categories:
                depth_categories[depth].append(category)
            else:
                depth_categories[depth] = [category]

        while True:

            current_category_name, depth = pop_category()
            if current_category_name is None: return articles
            # quit if max_depth reached
            if max_depth is not None and depth >= max_depth: continue
            # quit if category has already been visited
            if current_category_name in closed_categories: continue

            current_category = category.Category(self.site, current_category_name)
            articles_found = 0
            sublinks = self.get_category_articles(current_category)
            random.shuffle(sublinks)  # shuffle sublinks

            for d in sublinks:
                if self.is_category(d.title) and d.title not in closed_categories:
                    push_category(d.title, depth+1)
                    current_max_depth = depth+1 if depth+1 > current_max_depth else current_max_depth
                else:  # d is in article

                    # break if max articles per subcategory reached (not relevant to root category)
                    if max_articles_per_subcategory is not None and depth == 0 and articles_found >= 50:
                        continue
                    if max_articles_per_subcategory is not None and depth > 0 and articles_found >= max_articles_per_subcategory:
                        continue

                    articles.add(self.attach_metadata(d))
                    articles_found += 1

                    # quit if maximum_articles_num reached
                    if max_articles_num is not None and len(articles) >= max_articles_num:
                        return articles

            closed_categories.add(current_category)

        #return articles



######## English
cf = CategoryFetcher('en')
articles = cf.get_category_recursively("Category:Institute_of_Physics")
for article in articles:
   print article

####### Spanish
cf = CategoryFetcher('es')
articles = cf.get_category_recursively('Categoría:Libros_de_ciencias_de_la_computación')
for article in articles:
   print article

# articles = get_category_recursively(site, "Categoría:Libros_de_física")
