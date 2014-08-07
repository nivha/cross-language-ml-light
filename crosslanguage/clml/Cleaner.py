# coding=utf-8
import os
import simplejson
from clml.utils import get_category_folder

__author__ = 'Mojo'



def clean_english_articles_with_spanish_parallels(en_category_name, es_category_name):
    """
    Iterates on english articles and for each english article,
    checks if there exists a spanish article which is the direct link from the english article.
    Removes those english articles..

    :param en_category_name: name of the english category to check
    :param es_category_name: name of the respective category in spanish

    """
    en_folder = get_category_folder('en', en_category_name)
    es_folder = get_category_folder('es', es_category_name)

    # collect original spanish urls from spanish category
    es_urls = set()
    for fname in os.listdir(es_folder):
        p = os.path.join(es_folder, fname)
        with open(p) as f:
            d = simplejson.loads(f.read())
            es_urls.add(d['original_url'])

    to_delete = []
    for fname in os.listdir(en_folder):
        p = os.path.join(en_folder, fname)
        with open(p) as f:
            d = simplejson.loads(f.read())
            if d['spanish_url'] in es_urls:
                to_delete.append(p)

    # delete them!
    for path in to_delete:
        print 'removing', path
        os.remove(path)

def clean_untranslated_articels(language, category_name):
    """ Clean articles that couldn't be translated """

    category_path = get_category_folder(language, category_name)
    other_lang = 'es' if language == 'en' else 'en'
    # get original language files
    orig = set(filter(lambda x: os.path.splitext(x)[-1]=='.txt', os.listdir(category_path)))
    trans = set(filter(lambda x: os.path.splitext(x)[-1]=='.txt', os.listdir(os.path.join(category_path, other_lang))))

    untranslated = orig - trans
    # delete untranslated
    for fname in untranslated:
        path = os.path.join(category_path, fname)
        print 'deleting', path
        os.remove(path)




#############################################################
#       Testing...                                          #
#############################################################

if __name__=="__main__":

    # clean_english_articles_with_spanish_parallels('Black_holes', 'Agujeros_negros')
    # clean_english_articles_with_spanish_parallels('Dark_matter', 'Materia_oscura')
    # en_cs = ['Black_holes', 'Dark_matter']
    # es_cs = ['Agujeros_negros', 'Materia_oscura']

    # clean_english_articles_with_spanish_parallels('Asian_art', 'Arte_de_Asia')
    # clean_english_articles_with_spanish_parallels('Latin_American_art', 'Arte_latinoamericano')
    # en_cs = ['Asian_art', 'Latin_American_art']
    # es_cs = ['Arte_de_Asia', 'Arte_latinoamericano']

    clean_english_articles_with_spanish_parallels('Epistemology', 'Epistemolog%C3%ADa')
    clean_english_articles_with_spanish_parallels('Ethics', '%C3%89tica')
    en_categories = ['Epistemology', 'Ethics']
    es_categories = ['Epistemología', 'Ética']

    # for c in en_cs:
    #     print c
    #     clean_untranslated_articels('en', c)
    # for c in es_cs:
    #     print c
    #     clean_untranslated_articels('es', c)