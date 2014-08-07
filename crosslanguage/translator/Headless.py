
__author__ = 'Mojo'


# import sys
# from PyQt4.QtWebKit import QWebPage, QWebView, QWebSettings, QWebFrame
# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QUrl, QObject, SIGNAL


# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# from PyQt4.QtWebKit import *

# class Render(QWebPage):
#   def __init__(self, url):
#     self.app = QApplication(sys.argv)
#     QWebPage.__init__(self)
#     self.loadFinished.connect(self._loadFinished)
#     self.mainFrame().load(QUrl(url))
#     self.app.exec_()
#
#   def _loadFinished(self, result):
#     self.frame = self.mainFrame()
#     self.app.quit()
#
# url = "http://www.spanishenglish.com/"
# r = Render(url)
# html = r.frame.toHtml()



#
# app = QApplication(sys.argv)
# web = QWebView()
# web.load(QUrl(url))
# f = lambda x: x
# # QObject.connect(web, SIGNAL("loadFinished"), f(4))
#



# import mechanize
# url = "http://www.spanishenglish.com/"
# browser = mechanize.Browser()
# browser.set_handle_robots(False)
# browser.open(url)


from spynner import Browser
browser = Browser()
from pyquery import PyQuery
browser.set_html_parser(PyQuery)
url = "http://www.spanishenglish.com/"
browser.load(url)
print "LOADED"
browser.click("a[href='#en']", wait_load=False)
browser.click("#LangPair_ToDDL tbody tr td a[href='#de']", wait_load=False)
browser.wk_fill("#InputText", "How are you doing today?")
browser.click_ajax("#TranslateButton")
import time
time.sleep(15)
result_box = browser.soup('#TranslationOutput')[0]
translated_text = result_box.text_content()
# browser.show()
time.sleep(30)
print '123'




from spynner import Browser
browser = Browser()
from pyquery import PyQuery
browser.set_html_parser(PyQuery)
# url = "http://www.spanishenglish.com/"
url = "https://translate.google.com/#en/es/The%20Cryogenic%20Dark%20Matter%20Search%20%28CDMS%29%20is%20a%20series%20of%20experiments%20designed%20directly%20to%20detect%20particle%20dark%20matter%20in%20the%20form%20of%20WIMPs.%20Using%20an%20array%20of%20semiconductor%20detectors%20at%20millikelvin%20temperatures,%20CDMS%20has%20set%20the%20most%20sensitive%20limits%20to%20date%20on%20the%20interactions%20of%20WIMP%20dark%20matter%20with%20terrestrial%20materials.%20The%20first%20experiment,%20CDMSI,%20was%20run%20in%20a%20tunnel%20under%20the%20Stanford%20University%20campus.%20The%20current%20experiment,%20SuperCDMS,%20is%20located%20deep%20underground%20in%20the%20Soudan%20Mine%20in%20northern%20Minnesota.==%20Background%20==Observations%20of%20the%20large-scale%20structure%20of%20the%20universe%20show%20that%20matter%20is%20aggregated%20into%20very%20large%20structures%20that%20would%20not%20have%20time%20to%20have%20formed%20under%20the%20force%20of%20their%20own%20self-gravitation.%20It%20is%20generally%20believed%20that%20some%20form%20of%20missing%20mass%20is%20responsible%20for%20increasing%20the%20gravitational%20force%20at%20these%20scales,%20although%20this%20mass%20has%20not%20been%20directly%20observed.%20This%20is%20a%20problem;%20normal%20matter%20in%20space%20will%20heat%20up%20until%20it%20gives%20off%20light,%20so%20if%20this%20missing%20mass%20exists,%20it%20is%20generally%20assumed%20to%20be%20in%20a%20form%20that%20is%20not%20commonly%20observed%20on%20earth.A%20number%20of%20proposed%20candidates%20for%20the%20missing%20mass%20have%20been%20put%20forward%20over%20time.%20Early%20candidates%20included%20heavy%20baryons%20that%20would%20have%20had%20to%20be%20created%20in%20the%20big%20bang,%20but%20more%20recent%20work%20on%20nucleosynthesis%20seems%20to%20have%20ruled%20most%20of%20these%20out.%20Another%20candidate%20are%20new%20types%20of%20particles%20known%20as%20weakly%20interacting%20massive%20particles,%20or%20%22WIMP%22s.%20As%20the%20name%20implies,%20WIMPs%20interact%20weakly%20with%20normal%20matter,%20which%20explains%20why%20they%20are%20not%20easily%20visible.Detecting%20WIMPs%20thus%20presents%20a%20problem;%20if%20the%20WIMPs%20are%20very%20weakly%20interacting,%20detecting%20them%20will%20be%20extremely%20difficult.%20Detectors%20like%20CDMS%20and%20similar%20experiments%20measure%20huge%20numbers%20of%20interactions%20within%20their%20detector%20volume%20in%20order%20to%20find%20the%20extremely%20rare%20WIMP%20events.==%20Detection%20technology%20==The%20CDMS%20detectors%20measure%20the%20ionization%20and%20phonons%20produced%20by%20every%20particle%20interaction%20in%20their%20germanium%20and%20silicon%20crystal%20substrates.%20These%20two%20measurements%20determine%20the%20energy%20deposited%20in%20the%20crystal%20in%20each%20interaction,%20but%20also%20give%20information%20about%20what%20kind%20of%20particle%20caused%20the%20event.%20%20The%20ratio%20of%20ionization%20signal%20to%20phonon%20signal%20differs%20for%20particle%20interactions%20with%20atomic%20electrons%20%28%22electron%20recoils%22%29%20and%20atomic%20nuclei%20%28%22nuclear%20recoils%22%29.%20%20The%20vast%20majority%20of%20background%20particle%20interactions%20are%20electron%20recoils,%20while%20WIMPs%20%28and%20neutrons%29%20are%20expected%20to%20produce%20nuclear%20recoils.%20%20This%20allows%20WIMP-scattering%20events%20to%20be%20identified%20even%20though%20they%20are%20rare%20compared%20to%20the%20vast%20majority%20of%20unwanted%20background%20interactions.From%20Supersymmetry,%20the%20probability%20of%20a%20spin-independent%20interaction%20between%20a%20WIMP%20and%20a%20nucleus%20would%20be%20related%20to%20the%20amount%20of%20nucleons%20in%20the%20nucleus.%20Thus,%20a%20WIMP%20would%20be%20more%20likely%20to%20interact%20with%20a%20germanium%20detector%20than%20a%20silicon%20detector,%20since%20germanium%20is%20a%20much%20heavier%20element.%20Neutrons%20would%20be%20able%20to%20interact%20with%20both%20silicon%20and%20germanium%20detectors%20with%20similar%20probability.%20By%20comparing%20rates%20of%20interactions%20between%20silicon%20and%20germanium%20detectors,%20CDMS%20is%20able%20to%20determine%20the%20probability%20of%20interactions%20being%20caused%20by%20neutrons.CDMS%20detectors%20are%20disks%20of%20germanium%20or%20silicon,%20cooled%20to%20millikelvin%20temperatures%20by%20a%20dilution%20refrigerator.%20%20The%20extremely%20low%20temperatures%20are%20needed%20to%20limit%20thermal%20noise%20which%20would%20otherwise%20obscure%20the%20phonon%20signals%20of%20particle%20interactions.%20%20Phonon%20detection%20is%20accomplished%20with%20superconduction%20transition%20edge%20sensors%20%28TESs%29%20read%20out%20by%20SQUID%20amplifiers,%20while%20ionization%20signals%20are%20read%20out%20using%20a%20FET%20amplifier.%20CDMS%20detectors%20also%20provide%20data%20on%20the%20phonon%20pulse%20shape%20which%20is%20crucial%20in%20rejecting%20near-surface%20background%20events.==%20History%20==Simultaneous%20detection%20of%20ionization%20and%20heat%20with%20semiconductors%20at%20low%20temperature%20was%20first%20proposed%20by%20Blas%20Cabrera,%20Lawrence%20M.%20Krauss,%20and%20Frank%20Wilczek.CDMS%20collected%20WIMP%20search%20data%20in%20a%20shallow%20underground%20site%20at%20Stanford%20University%20through%202002,%20and%20has%20operated%20%28with%20collaboration%20from%20the%20University%20of%20Minnesota%29%20in%20the%20Soudan%20Mine%20since%202003.%20A%20new%20detector%20with%20interleaved%20electrodes,%20more%20mass,%20and%20even%20better%20background%20rejection%20is%20currently%20taking%20data%20at%20Soudan,%20under%20the%20name%20of%20SuperCDMS.===Results===On%20December%2017,%202009,%20the%20collaboration%20announced%20the%20possible%20detection%20of%20two%20candidate%20WIMPs,%20one%20on%20August%208,%202007%20and%20the%20other%20on%20October%2027,%202007.%20However,%20due%20to%20this%20low%20number%20of%20events,%20the%20team%20could%20not%20claim%20that%20the%20detections%20were%20true%20WIMPs;%20they%20may%20have%20been%20false%20positives%20from%20background%20noise%20such%20as%20neutron%20collisions.%20%20It%20is%20estimated%20that%20such%20noise%20would%20produce%20two%20or%20more%20events%2025%%20of%20the%20time.%20Polythene%20absorbers%20were%20fitted%20to%20reduce%20any%20neutron%20background.A%202011%20analysis%20of%20the%20data,%20with%20lower%20energy%20thresholds,%20looked%20for%20evidence%20for%20low-mass%20WIMPs%20%28M%20%3C%209%20GeV%29.%20%20Their%20limits%20rule%20out%20hints%20claimed%20by%20a%20new%20germanium%20experiment%20called%20CoGeNT%20and%20the%20long-standing%20DAMA%20result%20based%20on%20annual%20modulation.A%20further%20analysis%20of%20data%20in%202013,%20revealed%203%20WIMP%20detections%20in%20a%20time%20period%20where%20a%20background%20reading%20of%200.7%20would%20be%20expected.%20Also,%20the%20detections%20have%20masses%20comparable%20to%20that%20expected%20from%20WIMPs,%20including%20neutralinos.%20There%20is%20a%200.19%%20chance%20that%20these%20detections%20are%20anomalous,%20and%20caused%20by%20the%20background%20noise,%20giving%20the%20result%20a%2099.8%%20%283%20sigma%29%20confidence%20level.%20Whilst%20not%20conclusive%20evidence%20for%20WIMPs%20this%20provides%20strong%20weight%20to%20the%20theories.%20The%20CDMS%20collaboration%20published%20these%20results%20in%20Physical%20Review%20Letters,%20in%20May%202013.==Proposed%20upgrades:%20SuperCDMS%20and%20GEODM==SuperCDMS%20is%20the%20successor%20to%20CDMS%20II.%20%20The%20%22super%22%20refers%20to%20the%20larger,%20improved%20detectors.%20%20There%20are%20actually%20three%20generations%20of%20Super%20CDMS%20planned:#%20SuperCDMS%20Soudan,%20with%209.3%20kg%20of%20active%20detector%20mass%20made%20of%2015%C3%97620%20g%20germanium%20discs%20%2876.2%20mm/3%E2%80%B3%20diameter%20%C3%97%2025.4%20mm/1%E2%80%B3%20thick%29.%20%20This%20has%20been%20operating%20since%20March%202012.#%20SuperCDMS%20SNOLAB,%20with%20100%E2%80%93200%20kg%20of%20active%20detector%20mass,%20made%20of%201380%20g%20germanium%20discs%20%28100%20mm/3.9%E2%80%B3%20diameter%20%C3%97%2033.3%20mm/1.3%E2%80%B3%20thick%29.%20%20Development%20is%20underway,%20and%20it%20is%20hoped%20construction%20will%20begin%20in%202014.%20%20The%20deeper%20SNOLAB%20site%20will%20reduce%20cosmic%20ray%20backgrounds%20compared%20to%20Soudan.#%20GEODM%20%28Germanium%20Observatory%20for%20Dark%20Matter%29,%20with%20more%20than%201000%20kg%20of%20detector%20mass.%20%20Preliminary%20planning%20hopes%20to%20install%20this%20in%20the%20DUSEL%20laboratory.Increasing%20the%20detector%20mass%20only%20makes%20the%20detector%20more%20sensitive%20if%20the%20unwanted%20background%20detections%20do%20not%20increase%20as%20well,%20thus%20each%20generation%20must%20be%20cleaner%20and%20better%20shielded%20than%20the%20one%20before.%20%20The%20purpose%20of%20building%20in%20ten-fold%20stages%20like%20this%20is%20to%20develop%20the%20necessary%20shielding%20techniques%20before%20finalizing%20the%20GEODM%20design.==References====External%20links==*CDMS%20web%20site"
browser.load(url)
result_box = browser.soup('#result_box')[0]
translated_text = result_box.text_content()



# import urllib2
#
# def translate(to_translate, to_langage="auto", langage="auto"):
#     '''Return the translation using google translate
#     you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
#     if you don't define anything it will detect it or use english by default
#     Example:
#     print(translate("salut tu vas bien?", "en"))
#     hello you alright?'''
#     agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
#     before_trans = 'class="t0">'
#     link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
#     request = urllib2.Request(link, headers=agents)
#     page = urllib2.urlopen(request).read()
#     result = page[page.find(before_trans)+len(before_trans):]
#     result = result.split("<")[0]
#     return result
#
# if __name__ == '__main__':
#     to_translate = 'Hola como estas?'
#     # to_translate = 'The Cryogenic Dark Matter Search %28CDMS%29 is a series of experiments designed directly to detect particle dark matter in the form of WIMPs. Using an array of semiconductor detectors at millikelvin temperatures, CDMS has set the most sensitive limits to date on the interactions of WIMP dark matter with terrestrial materials. The first experiment, CDMSI, was run in a tunnel under the Stanford University campus. The current experiment, SuperCDMS, is located deep underground in the Soudan Mine in northern Minnesota.== Background ==Observations of the large-scale structure of the universe show that matter is aggregated into very large structures that would not have time to have formed under the force of their own self-gravitation. It is generally believed that some form of missing mass is responsible for increasing the gravitational force at these scales, although this mass has not been directly observed. This is a problem; normal matter in space will heat up until it gives off light, so if this missing mass exists, it is generally assumed to be in a form that is not commonly observed on earth.A number of proposed candidates for the missing mass have been put forward over time. Early candidates included heavy baryons that would have had to be created in the big bang, but more recent work on nucleosynthesis seems to have ruled most of these out. Another candidate are new types of particles known as weakly interacting massive particles, or %22WIMP%22s. As the name implies, WIMPs interact weakly with normal matter, which explains why they are not easily visible.Detecting WIMPs thus presents a problem; if the WIMPs are very weakly interacting, detecting them will be extremely difficult. Detectors like CDMS and similar experiments measure huge numbers of interactions within their detector volume in order to find the extremely rare WIMP events.== Detection technology ==The CDMS detectors measure the ionization and phonons produced by every particle interaction in their germanium and silicon crystal substrates. These two measurements determine the energy deposited in the crystal in each interaction, but also give information about what kind of particle caused the event.  The ratio of ionization signal to phonon signal differs for particle interactions with atomic electrons %28%22electron recoils%22%29 and atomic nuclei %28%22nuclear recoils%22%29.  The vast majority of background particle interactions are electron recoils, while WIMPs %28and neutrons%29 are expected to produce nuclear recoils.  This allows WIMP-scattering events to be identified even though they are rare compared to the vast majority of unwanted background interactions.From Supersymmetry, the probability of a spin-independent interaction between a WIMP and a nucleus would be related to the amount of nucleons in the nucleus. Thus, a WIMP would be more likely to interact with a germanium detector than a silicon detector, since germanium is a much heavier element. Neutrons would be able to interact with both silicon and germanium detectors with similar probability. By comparing rates of interactions between silicon and germanium detectors, CDMS is able to determine the probability of interactions being caused by neutrons.CDMS detectors are disks of germanium or silicon, cooled to millikelvin temperatures by a dilution refrigerator.  The extremely low temperatures are needed to limit thermal noise which would otherwise obscure the phonon signals of particle interactions.  Phonon detection is accomplished with superconduction transition edge sensors %28TESs%29 read out by SQUID amplifiers, while ionization signals are read out using a FET amplifier. CDMS detectors also provide data on the phonon pulse shape which is crucial in rejecting near-surface background events.== History ==Simultaneous detection of ionization and heat with semiconductors at low temperature was first proposed by Blas Cabrera, Lawrence M. Krauss, and Frank Wilczek.CDMS collected WIMP search data in a shallow underground site at Stanford University through 2002, and has operated %28with collaboration from the University of Minnesota%29 in the Soudan Mine since 2003. A new detector with interleaved electrodes, more mass, and even better background rejection is currently taking data at Soudan, under the name of SuperCDMS.===Results===On December 17, 2009, the collaboration announced the possible detection of two candidate WIMPs, one on August 8, 2007 and the other on October 27, 2007. However, due to this low number of events, the team could not claim that the detections were true WIMPs; they may have been false positives from background noise such as neutron collisions.  It is estimated that such noise would produce two or more events 25% of the time. Polythene absorbers were fitted to reduce any neutron background.A 2011 analysis of the data, with lower energy thresholds, looked for evidence for low-mass WIMPs %28M %3C 9 GeV%29.  Their limits rule out hints claimed by a new germanium experiment called CoGeNT and the long-standing DAMA result based on annual modulation.A further analysis of data in 2013, revealed 3 WIMP detections in a time period where a background reading of 0.7 would be expected. Also, the detections have masses comparable to that expected from WIMPs, including neutralinos. There is a 0.19% chance that these detections are anomalous, and caused by the background noise, giving the result a 99.8% %283 sigma%29 confidence level. Whilst not conclusive evidence for WIMPs this provides strong weight to the theories. The CDMS collaboration published these results in Physical Review Letters, in May 2013.==Proposed upgrades: SuperCDMS and GEODM==SuperCDMS is the successor to CDMS II.  The %22super%22 refers to the larger, improved detectors.  There are actually three generations of Super CDMS planned:# SuperCDMS Soudan, with 9.3 kg of active detector mass made of 15%C3%97620 g germanium discs %2876.2 mm/3%E2%80%B3 diameter %C3%97 25.4 mm/1%E2%80%B3 thick%29.  This has been operating since March 2012.# SuperCDMS SNOLAB, with 100%E2%80%93200 kg of active detector mass, made of 1380 g germanium discs %28100 mm/3.9%E2%80%B3 diameter %C3%97 33.3 mm/1.3%E2%80%B3 thick%29.  Development is underway, and it is hoped construction will begin in 2014.  The deeper SNOLAB site will reduce cosmic ray backgrounds compared to Soudan.# GEODM %28Germanium Observatory for Dark Matter%29, with more than 1000 kg of detector mass.  Preliminary planning hopes to install this in the DUSEL laboratory.Increasing the detector mass only makes the detector more sensitive if the unwanted background detections do not increase as well, thus each generation must be cleaner and better shielded than the one before.  The purpose of building in ten-fold stages like this is to develop the necessary shielding techniques before finalizing the GEODM design.==References====External links==*CDMS web site'
#     to_translate = 'The cuspy halo problem arises from cosmological simulations that seem to indicate cold dark matter %28CDM%29 would form cuspy distributions %26mdash%3B that is%2C increasing sharply to a high value at a central point %26mdash%3B in the most dense areas of the universe. This would imply that the center of our galaxy%2C for example%2C should exhibit a higher dark-matter density than other areas. However%2C it seems rather that the centers of these galaxies likely have no cusp in the dark-matter distribution at all.%0A%0AThis remains an intractable problem.  Speculation that the distribution of baryonic matter may somehow displace cold dark matter in the dense cores of spiral galaxies has not been substantiated by any plausible explanation or computer simulation.%0A%0A%3D%3DSimulation Results%3D%3D%0A%0A%22The presence of a cusp in the centers of CDM halos is one of the earliest and strongest results derived from N-body cosmological simulations.%22 Numerical simulations for CDM structure formation predict some structure properties that conflict with astronomical observations.%0A%0A%3D%3DObservations%3D%3D%0A%0AThe discrepancies range from galaxies to clusters of galaxies. %22The main one that has attracted a lot of attention is the cuspy halo problem%2C namely that CDM models predict halos that have a high density core or have an inner profile that is too steep compared to observations.%22%0A%0A%3D%3DPotential Solutions%3D%3D%0A%0AThe conflict between numerical simulations and astronomical observations creates numerical constraints related to the core/cusp problem. Observational constraints on halo concentrations imply the existence of theoretical constraints on cosmological parameters. According to McGaugh%2C Barker%2C and de Blok%2C there might be 3 basic possibilities for interpreting the halo concentration limits stated by them or anyone else%3A%0A%23%22CDM halos must have cusps%2C so the stated limits hold and provide new constraints on cosmological parameters.%22%0A%23%22Something %28e.g. feedback%2C modifications of the nature of dark matter%29 eliminates cusps and thus the constraints on cosmology.%22%0A%23 %22The picture of halo formations suggested by CDM simulations is wrong.%22%0A%0AOne approach to solving the cusp-core problem in galactic halos is to consider models that modify the nature of dark matter%3B theorists have considered warm%2C fuzzy%2C self-interacting%2C and meta-cold dark matter%2C among other possibilities.%0A%0A%3D%3DReferences%3D%3D%0A%0A%3D%3DSee also%3D%3D%0A%2ADwarf galaxy problem %28also known as %22the missing satellites problem%22%29%0A%2AList of unsolved problems in physics'
#     #print("%s >> %s" % (to_translate, translate(to_translate)))
#     #print("%s >> %s" % (to_translate, translate(to_translate, 'fr')))
#     print translate(to_translate[:2066], 'es', 'en')
#     #should print Hola como estas >> Hello how are you
#     # #and Hola como estas? >> Bonjour comment allez-vous?


print '123'
