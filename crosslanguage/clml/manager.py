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
    #
    load_category(src_language, src_c)
    load_category(dst_language, dst_c)



# download_cateogries('en', 'es', 'Religion', 'Religión')
# download_cateogries('en', 'es', 'Epistemology', 'Epistemología')
# download_cateogries('en', 'es', 'Ethics', 'Ética')
# download_cateogries('en', 'es', 'Marxism', 'Marxismo')
# download_cateogries('en', 'es', 'Anarchism', 'Anarquismo')
# download_cateogries('en', 'es', 'Religion', 'Religión')
# download_cateogries('en', 'es', 'Spirituality', 'Espiritualidad')
# download_cateogries('en', 'es', 'Islamic_architecture', 'Arquitectura_islámica')
download_cateogries('en', 'es', 'Modernist_architecture', 'Arquitectura_moderna')
