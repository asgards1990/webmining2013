#! /usr/bin/env python
# -*- coding: latin-1 -*-

import Extractor.superExtractor
from Extractor.extractorHTML import ExtractorHTML

import urllib

import Extractor.customisedCleaner as CustomCleaner

page = urllib.urlopen('http://www.lemonde.fr/')
t = page.read()

cleaner = CustomCleaner.CustomedCleaner_HTML()

Ex = ExtractorHTML(t,cleaner)
#Extraction du titre
#Ex.extractTitle()

#Extraction des tag H1, H2, H3
#Ex.extractH1()
#Ex.extractH2()
#Ex.extractH3()

#Extraction des tags Strong et Em
#Ex.extractStrong()
#Ex.extractEm()

#Extraction des Links + contenu des links
Ex.extractLink()

#Extraction des balises des images
Ex.extractImgAlt()

#Extraction des meta données
print Ex.extractMetaDescription()
