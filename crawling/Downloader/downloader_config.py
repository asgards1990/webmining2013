#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Définit la configuration du module Downloader

#Loggers
DOWNLOADER_LOGGER_NAME = "DOWNLOADER"
IMDB_DOWNLOADER_LOGGER_NAME = "IMDB DOWNLOADER"
IMDB_FILM_DOWNLOADER_LOGGER_NAME = "IMDB FILM DOWNLOADER"


#PATHS
IMDB_FILM_ROOT = "/home/hollocou/tests/imdb/film/" # "/home/pesto/imdb/film/"
IMDB_FILM_MAINPAGE_SUBPATH = "mainpage/"
IMDB_FILM_FULLCREDITS_SUBPATH = "fullcredits/"
IMDB_FILM_AWARDS_SUBPATH = "awards/"
IMDB_FILM_REVIEWS_SUBPATH = "reviews/"
IMDB_FILM_KEYWORDS_SUBPATH = "keywords/"
IMDB_FILM_COMPANYCREDITS_SUBPATH = "companycredits/"
IMDB_PERSON_ROOT = "/home/pesto/imdb/person/"
IMDB_COMPANY_ROOT = "/home/pesto/imdb/company/"

DOWNLOADER_MIN_PAGE_SIZE = 10000

IMDB_FILM_DOWNLOADER_MAX_REQUESTS_LIMIT = 10
