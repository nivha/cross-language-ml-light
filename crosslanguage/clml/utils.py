import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from crosslanguage import settings


class Language(object):
    """
    An all-purpose language object (sort of an ENUM).
    If you wish to add a language, add and update all following dicionaries.
    """
    English = 'English'
    Spanish = 'Spanish'
    Hebrew = 'Hebrew'
    Portuguese = 'Portuguese'

    # For each language, how it is represented in Wikipedia's URLs.
    # This is also the path of the files on the hard drive.
    lang_to_path = {
        English: 'en',
        Spanish: 'es',
        Hebrew: 'he',
        Portuguese: 'pt'
    }
    #
    path_to_lang = {
        'en': English,
        'es': Spanish,
        'he': Hebrew,
        'pt': Portuguese
    }

    # This is how the language is represented in Google Translate URLs.
    lang_to_google_translate = {
        English: 'en',
        Spanish: 'es',
        Hebrew: 'iw',
    }

    def __init__(self, lang, path_lang=None):
        if path_lang is None:
            self.lang = lang
        else:
            self.lang = Language.path_to_lang[path_lang]

    def to_path(self):
        return self.lang_to_path[self.lang]

    def to_google_translate(self):
        return self.lang_to_google_translate[self.lang]

    def __str__(self):
        return self.lang

    def __repr__(self):
        return str(self)


def get_category_folder(language,  category_name):
    """
    :param category_name: name of wanted category
    :return: full path to where this category should be found in fs
    """
    return os.path.join(settings.DATA_DIR, language, category_name)


