#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""Definit la classe parent de tous les extractors. Les extractors définissent les fonctions qui  permettent d'extraire des données des documents. Il existe un Extractor par type de documents (HTML, XML,...)"""


class SuperExtractor:
   def __init__(self,string):
      self.string = string
      self.parser = None
      



