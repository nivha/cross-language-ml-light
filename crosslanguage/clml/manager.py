# coding=utf-8
import os
import urllib
from clml.Cleaner import clean_untranslated_articels, clean_english_articles_with_spanish_parallels

from clml.data_load import load_category
from clml.utils import get_category_folder, Language
from fetcher.WikiFetcher import WikiFetcher
from translator.TranslateAll import CategoryTranslator


__author__ = 'Niv & Ori'


def download_cateogries(src_language, dst_language, src_c, dst_c):

    WikiFetcher(src_language, src_c, 1000, None, 25).fetch_to_files()
    WikiFetcher(dst_language, dst_c, 400, None, 25).fetch_to_files()

    src_c = urllib.quote(src_c)
    dst_c = urllib.quote(dst_c)
    clean_english_articles_with_spanish_parallels(src_c, dst_c)

    src_lang = Language(Language.path_to_lang[src_language])
    dst_lang = Language(Language.path_to_lang[dst_language])
    CategoryTranslator(src_lang, [dst_lang], src_c).do_translation()
    CategoryTranslator(dst_lang, [src_lang], dst_c).do_translation()

    load_category(src_language, src_c)
    load_category(dst_language, dst_c)


# en_cs = ['Epistemology', 'Ethics', 'Dark_matter', 'Black_holes', 'Asian_art', 'Latin_American_art']
# es_cs = ['Epistemolog%C3%ADa', '%C3%89tica', 'Materia_oscura', 'Agujeros_negros', 'Arte_de_Asia', 'Arte_latinoamericano']

# [Anthropology, Sociology]
# [Antropología, Sociología]

# [Religion, Religión]
# [Spirituality, Espiritualidad]

# [Marxism, Marxismo]
# [Anarchism, Anarquismo]

# download_cateogries('en', 'es', 'Religion', 'Religión')

load_category('en', 'Spirituality')
load_category('es', 'Espiritualidad')

load_category('en', 'Religion')
load_category('es', urllib.quote('Religión'))
