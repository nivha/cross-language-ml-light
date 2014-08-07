import os
from clml.Cleaner import clean_untranslated_articels

from clml.data_load import load_category
from clml.utils import get_category_folder


__author__ = 'Niv & Ori'


def download_cateogries(language, categories, max_articles_num):

    # for category in categories:
    #     wf = WikiFetcher(language, category, max_articles_num)
    #     wf.fetch_to_files()

    # for c in es_categories:
    #     tr = CategoryTranslator(Language(Language.Spanish), [Language(Language.English)], c)
    #     tr.do_translation()
    pass



en_cs = ['Epistemology', 'Ethics', 'Dark_matter', 'Black_holes', 'Asian_art', 'Latin_American_art']
es_cs = ['Epistemolog%C3%ADa', '%C3%89tica', 'Materia_oscura', 'Agujeros_negros', 'Arte_de_Asia', 'Arte_latinoamericano']


for c in en_cs:
    # clean_untranslated_articels('en', c)
    load_category('en', c)
for c in es_cs:
    # clean_untranslated_articels('es', c)
    load_category('es', c)
