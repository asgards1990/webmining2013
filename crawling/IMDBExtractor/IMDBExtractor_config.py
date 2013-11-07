#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Définit la configuration du module Extractor

#Logger
IMDB_EXTRACTOR_LOGGER_NAME = "EXTRACTOR IMDB"
EXTRACTOR_LOGGER_NAME = "EXTRACTOR IMDB -- Extract script"

LOCAL_PATH="/home/pesto/imdb/"

FILM_URL= LOCAL_PATH + "film/mainpage/{}.html"
PERSON_URL=LOCAL_PATH+"person/{}.html"
FULL_CREDITS_URL=LOCAL_PATH+"film/fullcredits/{}.html"
COMPANY_CREDITS_URL=LOCAL_PATH+"film/companycredits/{}.html"
REVIEWS_URL=LOCAL_PATH+"film/reviews/{}.html"
KEYWORDS_URL=LOCAL_PATH+"film/keywords/{}.html"
AWARDS_URL=LOCAL_PATH+"film/awards/{}.html"
COMPANY_URL=LOCAL_PATH+"company/{}.html"

POSTER_PATH="/home/pesto/imdb/poster/"
POSTER_PATH="/home/pesto/imdb/person_pic/"
