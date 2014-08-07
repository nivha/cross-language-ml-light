import os
import urllib
import urllib2
import simplejson

os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from clml.utils import Language
from spynner import Browser
from pyquery import PyQuery

import codecs
import httplib
import traceback
from threading import Timer


# TODO: wrap the selenium with 'with'
class FileTranslator(object):

    def __init__(self, source_lang, target_lang, translate_type='headless'):
        self.source_lang = source_lang
        self.target_lang = target_lang

        # instantiate the relevant browser for the instance
        self.headless_browser = self.driver = None
        if translate_type == 'headless':
            self.headless_browser = Browser()
            self.headless_browser.set_html_parser(PyQuery)
        elif translate_type == 'selenium':
            self.driver = webdriver.Firefox()

        # determine the kind of translator needed
        self.translate = {
            'simple': self.translate_simple,
            'headless': self.translate_text_google_headless,
            'selenium': self.translate_text_google
        }[translate_type]

    def _forcefully_kill_firefox(self):
        """ This is needed in order to kill Firefox when it gets stuck.. """
        print "Killing Firefox forcefully..."
        os.system('taskkill /im firefox.exe /f /t')

    def translate_text_google(self, text_to_translate, quit_browser=True):
        """
            Uses selenium to translate the text. kinda slow, and gets stuck..
        """
        # Open Google Translate website
        url = "http://translate.google.com/#%s/%s/%s" % (self.source_lang.to_google_translate(),
                                                         self.target_lang.to_google_translate(),
                                                         text_to_translate)
        self.driver.get(url)

        # Wait for results to appear and retrieve them
        # If results don't show up in 11 seconds, it means that Firefox stuck, kill it and continue
        t = Timer(11.0, self._forcefully_kill_firefox)
        t.start()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='result_box']/span[@class='hps']")))
        t.cancel()

        result = self.driver.find_element_by_id('result_box')
        translated_text = result.text
        self.driver.get('http://www.google.com')
        return translated_text

    def translate_text_google_headless(self, text_to_translate):
        """
            Uses spynner - a headless browser, to translate the text.
            This works really fast...
        """
        url = "https://translate.google.com/#%s/%s/%s" % (self.source_lang.to_google_translate(),
                                                          self.target_lang.to_google_translate(),
                                                          text_to_translate)
        self.headless_browser.load(url)
        result_box = self.headless_browser.soup('#result_box')[0]
        translated_text = result_box.text_content()
        self.headless_browser.load('http://www.example.com/')
        return translated_text

    def translate_simple(self, text_to_translate):
        """
            Uses simple urllib to translte.
            It doesn't really work on more than 2000 characters for some reason (maybe a limit posed by google)
        """
        '''Return the translation using google translate
        you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
        if you don't define anything it will detect it or use english by default
        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?'''
        agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
        before_trans = 'class="t0">'
        link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (self.target_lang.to_google_translate(),
                                                                   self.source_lang.to_google_translate(),
                                                                   text_to_translate.replace(" ", "+"))
        request = urllib2.Request(link, headers=agents)
        page = urllib2.urlopen(request).read()
        result = page[page.find(before_trans)+len(before_trans):]
        result = result.split("<")[0]
        return result

    def translate_text_spanishenglish(self, text_to_translate):
        """
            An attempt to use spynner to translate through spanishenglish.com
            (instead of google.. in case google will block us or something..)
            The problem is that for some reason spanishenglish.com doesn't work with the
            spynner core (it does work well with chrome though)... so it's stuck now...
        """
        pass
        # url = "http://www.spanishenglish.com/"
        # self.headless_browser.load(url)
        # print "LOADED"
        # self.headless_browser.click("a[href='#en']", wait_load=False)
        # self.headless_browser.click("#LangPair_ToDDL tbody tr td a[href='#de']", wait_load=False)
        # self.headless_browser.wk_fill("#InputText", "How are you doing today?")
        # self.headless_browser.click_ajax("#TranslateButton")
        #
        # import time
        # #time.sleep(15)
        # result_box = self.headless_browser.soup('#OutputTextHtmlCell')[0]
        # translated_text = result_box.text_content()
        # return translated_text
        #
        # # self.headless_browser.show()
        # # time.sleep(30)

    def translate_file(self, path):
        with open(path) as f:
            json = f.read()
            d = simplejson.loads(json)
            text = d['text']

            return self.translate(text)

    def translate_to_file(self, source_path, target_path):
        try:
            translated_text = self.translate_file(source_path)
        except httplib.CannotSendRequest:
            self.driver = webdriver.Firefox()
            return
        except Exception, e:
            print "Failed to translate: {:s}".format(source_path)
            print '='*60
            import traceback
            print traceback.format_exc()
            return

        with codecs.open(target_path, 'w', 'utf-8') as f:
            f.write(translated_text)


if __name__ == '__main__':
    # translator = FileTranslator(Language(Language.English), Language(Language.Spanish))
    # source_path = os.path.join(settings.DATA_DIR, 'en', 'Maxwell_Medal_and_Prize_recipients', 'Artur_Ekert.txt')
    # target_path = os.path.join(settings.DATA_DIR, 'en', 'Maxwell_Medal_and_Prize_recipients', 'es', 'Artur_Ekert.txt')
    #
    # translator.translate_to_file(source_path, target_path)

    translator = FileTranslator(Language(Language.English), Language(Language.Spanish))
    q = translator.translate_text_spanishenglish("Hi there boy")
    print q



###
               # # Initialize firefox friver
            # driver = webdriver.Firefox()
            # # Open Google Translate website
            # driver.get("http://translate.google.com/")
            # # Select source language
            # driver.find_element_by_id("gt-sl-gms").click()
            # driver.find_element_by_xpath(r'//div[contains(text_to_translate(), "{0}") and @class="goog-menuitem-content"]'
            #                              .format(source_lang)).click()
            # # Select target language
            # driver.find_element_by_id("gt-tl-gms").click()
            # driver.find_elements_by_xpath(r'//div[contains(text_to_translate(), "{0}") and @class="goog-menuitem-content"]'
            #                               .format(target_lang))[1].click()
            #
            # # Write input into box
            # source = driver.find_element_by_id('source')
            # source.send_keys(text_to_translate)
            #
            # time.sleep(10)

###

    # print translate_text(source_lang, target_lang, text)

# driver = webdriver.Firefox()

# driver.get("http://imtranslator.net/translation/english/to-spanish/translation/")
# text = driver.find_element_by_name("source")
# text.send_keys("school")
# google_tab = driver.find_element_by_id("google")
# t = google_tab.find_element_by_tag_name("span")
# t.click()

# #wait = ui.WebDriverWait(self.driver,10)
# element = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.ID, "tts2"))
# )
# #wait.until(lambda driver: driver.title.lower().startswith('course details'))

# target = driver.find_element_by_id("target")
# translated = target.get_attribute("value")
# print translated

# driver.quit()


##import mechanize
##
##class Element_by_id(object):
##    def __init__(self, id_text):
##        self.id_text = id_text
##    def __call__(self, f, *args, **kwargs):
##        return 'id' in f.attrs and f.attrs['id'] == self.id_text
##
##    
##
##b = mechanize.Browser()
##b.open("http://imtranslator.net/translation/english/to-spanish/translation/")
##b.select_form(nr=0)
##text = b.form.find_control(id="source")
##text = "work"
##
##s = b.response().read()
##f = open(r"C:\Users\niv\technion\bla.html", 'w')
##f.write(s)
##f.close()

