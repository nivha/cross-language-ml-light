# coding=utf-8

import os
import simplejson

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'

import urllib
import urllib2
from bs4 import BeautifulSoup
from wiki2plain import Wiki2Plain
from django.conf import settings
from fetcher.CategoryFetcher import CategoryFetcher


class FetcherError(Exception):
    pass

class WikiFetcher(object):
    """
        Fetch all articles in a Wikipedia Category
        Save each article to a file in the project's storage hierarchy

        Code example:

            # wf = WikiFetcher('en', "Institute_of_Physics")
            # wf = WikiFetcher('en', "International_Young_Physicists'_Tournament")
            wf = WikiFetcher('es', "Libros_de_ciencias_de_la_computación")
            wf.fetch_to_files()
    """

    def __init__(self, language, category, max_articles_num=None, max_depth=None, max_articles_per_subcategory=None):
        self.category = category
        self.language = language
        self.max_articles_num = max_articles_num
        self.max_depth = max_depth
        self.max_articles_per_subcategory = max_articles_per_subcategory

        self.category_base_dir = os.path.join(settings.DATA_DIR, self.language, urllib.quote_plus(self.category))

    def quote(self, x):
        return urllib.quote_plus(urllib.unquote(x))

    def fetch_raw_articles(self):
        cf = CategoryFetcher(self.language)
        return cf.get_category_recursively(self.category, self.max_articles_num, self.max_depth,
                                           self.max_articles_per_subcategory)

    def get_lang_links(self, page_url):
        """ returns dictionary of language->url for all links to other languages of this page """
        page = urllib2.urlopen(page_url)
        soup = BeautifulSoup(page)
        lang_links = {}
        for el in soup.select('li.interlanguage-link > a'):
            url = el.get('href')
            title = url[24:]
            title = self.quote(title)
            lang_links[el.get('lang')] = url[:24] + title
        return lang_links

    def extract_clean_text(self, article):
        raw_text = article.getWikiText()
        raw_text = unicode(raw_text, 'utf-8')

        # clean text - leave only wiki text
        clean_text = Wiki2Plain(raw_text, self.language).text
        clean_text = clean_text.encode('utf8')
        return clean_text

    def get_article_dic(self, article):
        """ prepare a nice looking json in this format:
                original-url: ...
                spanish-url: ...
                text: ...
        """


        quoted_title = self.quote(article.urltitle)
        path = os.path.join(self.category_base_dir, "{:s}.txt".format(quoted_title))
        clean_text = self.extract_clean_text(article)

        # get spanish link (only for english ones..)
        lang_links = self.get_lang_links(article.url)
        spanish_url = ''
        if self.language == 'en' and 'es' in lang_links:
            spanish_url = lang_links['es']

        # create json
        final = {
            'path': path,
            'original_url': article.url[5:],
            'spanish_url': spanish_url,
            'text': clean_text,
        }
        return final


    def fetch_to_files(self):
        """
            Save all category's articles into files in the relevant place
        """
        if not os.path.exists(self.category_base_dir): os.makedirs(self.category_base_dir)
        articles = self.fetch_raw_articles()
        print 'Fetched {:d} articles'.format(len(articles))
        for article in articles:
            article_dic = self.get_article_dic(article)
            path = article_dic.pop('path')
            print 'saving', path
            json = simplejson.dumps(article_dic)
            with open(path, "w") as f:
                f.write(json)


if __name__=="__main__":

    import cProfile

    # wf = WikiFetcher('en', "Institute_of_Physics")
    # wf = WikiFetcher('en', "International_Young_Physicists'_Tournament")
    # wf = WikiFetcher('es', "Libros_de_ciencias_de_la_computación")
    # wf = WikiFetcher('es', "Sistemas_de_gestión_empresarial_libres").fetch_to_files()
    # wf = cProfile.run("WikiFetcher('en', 'Aetobatus').fetch_to_files()")

    # some real shit now:
    # en_categories = ['Dark_matter', 'Black_holes']
    # es_categories = ['Materia_oscura', 'Agujeros_negros']

    # en_categories = ['Asian_art', 'Latin_American_art']
    # es_categories = ['Arte_de_Asia', 'Arte_latinoamericano']

    en_categories = ['Cognitive_biases', 'Epistemological_theories']
    es_categories = ['Sesgos_cognitivos', 'Teorías_epistemológicas']

    for category in en_categories:
        print category
        wf = WikiFetcher('en', category, 300, None, 10).fetch_to_files()
        # cProfile.run('wf.fetch_to_files()')
    for category in es_categories:
        print category
        wf = WikiFetcher('es', category, 200, None, 10).fetch_to_files()







