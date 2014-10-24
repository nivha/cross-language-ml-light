root directory:
	manage.py - Django manager
	shell.py - Wrapper file for running django shell
    
crosslanguage directory:
[contains general django settings.]

clml directory:
[defines database structure and database main actions]
    models.py - defines Django database models.
    admin.py - definitions  and settings for Django admin interface.
    utils.py  - various utilities and enums for other files.
    data_load.py - loads the downloaded article files and their translations to the database.
    Cleaner.py - cleans data and prepares it for experiments
    manager.py - combines the flow of adding data to the DB (scraping, translating and loading).

fetcher directory:
[scraping wikipedia and saving articles to files]
    utils.py  - various utilities and enums for other files.
    CategoryFetcher.py - Wraps the 'wikitools' library, and implements the wikipedia crawling and scraping.
    wiki2plain.py - Implements helper functions to clean the fetched articles from unnecessary data.
    WikiFetcher.py - Wraps the fetching + cleaning process.
    
translator directory:
[scraping google translate to translate the fetched articles]
    FileTranslator.py - Wraps a headless browser to reach Google Translate to translate a single file.
    TranslateAll.py - Goes over a relevant category to translate all the wanted files.
    
learning directory:
[implements the one-language classifier and the cross-language classifier and tester]
    SimpleClassifier.py - classifier and tester for articles in a single language.
    CrossLanguageClassifier.py - classifier for cross-language learning.
    CVHandler.py - class for handling cross validation and dividing the space into training and testing sets.
   
experiments directory:
[implements project experiments]
    Experiment1.py - implements experiment 1
    Experiment1.py - implements experiment 2
    utils.py - implements various helper functions, for extracting data from DB
    
experiments/shuffled directory:
[contains the shuffled order of documents for each experiments.]
    



    


	

