import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from translator.FileTranslator import FileTranslator

from clml.utils import Language


class CategoryTranslator(object):
    """
    Translate a category in a source language to several target languages.
    """

    def __init__(self, source_lang, target_lang_list, category_name):
        # Get path string for each language
        self.source_lang = source_lang
        self.target_lang_list = target_lang_list
        self.category_path = os.path.join(settings.DATA_DIR, source_lang.to_path(), category_name)

    def do_translation(self):
        target_lang_path_list = [l.to_path() for l in self.target_lang_list]

        # First, remove folders with any translated content
        # for folder in os.listdir(self.category_path):
        #     if folder in target_lang_path_list:
        #         shutil.rmtree(os.path.join(self.category_path, folder))

        # Then, translate all files for each language
        for target_lang in self.target_lang_list:
            # Determine directory for translations
            target_path = os.path.join(self.category_path, target_lang.to_path())

            # Delete old folder of translations
            # if os.path.isdir(target_path):
            #     shutil.rmtree(target_path)
            #     time.sleep(5)

            # Make new directory for translated articles
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            # Make translator
            translator = FileTranslator(self.source_lang, target_lang)

            # Translate all files in directory
            for filename in os.listdir(self.category_path):
                # Skip files which are not text files (ends with .txt)
                if not filename.endswith('.txt'): continue

                file_source_path = os.path.join(self.category_path, filename)
                file_target_path = os.path.join(target_path, filename)

                # don't translate if translation already exists
                if os.path.exists(file_target_path): continue

                # Translate source file to target file
                translator.translate_to_file(file_source_path, file_target_path)


def translate_all_lang_categories(source_lang, target_lang_list):
    """
    Translate all categories of a given language
    """
    source_lang_path = os.path.join(settings.DATA_DIR, source_lang.to_path())
    for category_name in os.listdir(source_lang_path):
        if not os.path.isdir(os.path.join(source_lang_path, category_name)):
            # Skip non-folders
            continue

        print 'Translating category: %s from %s to %r' % (category_name, source_lang, target_lang_list)
        CategoryTranslator(source_lang, target_lang_list, category_name).do_translation()
        print '> Done!'


class DataTranslator(object):
    """
    Translates all data in the system
    """
    def __init__(self):
        pass


if __name__ == '__main__':
    # translate_all_lang_categories(Language(Language.Spanish), [Language(Language.English)])
    # translate_all_lang_categories(Language(Language.English), [Language(Language.Spanish)])

    # en_categories = ['Asian_art', 'Latin_American_art']
    # es_categories = ['Arte_de_Asia', 'Arte_latinoamericano']

    # en_categories = ['Dark_matter', 'Black_holes']
    # es_categories = ['Materia_oscura', 'Agujeros_negros']

    en_categories = ['Epistemology', 'Ethics']
    es_categories = ['Epistemolog%C3%ADa', '%C3%89tica']

    # for c in en_categories:
    #     print c
    #     tr = CategoryTranslator(Language(Language.English), [Language(Language.Spanish)], c)
    #     tr.do_translation()
    # for c in es_categories:
    #     print c
    #     tr = CategoryTranslator(Language(Language.Spanish), [Language(Language.English)], c)
    #     tr.do_translation()


    CategoryTranslator(Language(Language.Spanish), [Language(Language.English)], 'Espiritualidad').do_translation()