#! /usr/bin/env python
# -*- coding: utf-8 -*-

from service.prodbox import *
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import csv

app = CinemaService()
app.loadData()
app.loadPredict()

X = app.predict_features

##################
### Box office ###
##################

def BoxOfficeScores():
    y = app.predict_labels_log_box_office.ravel()
    y_bin = y > np.median(y)

    # CLASSIFICATION

    print('\nClassification by random forest for the Box Office...')
    clf = RandomForestClassifier()
    scores = cross_val_score(clf, X, y_bin, cv=3)
    print 'Classification by random forest score: ', scores.mean()

    print('\nClassification by gradient boosting for the Box Office...')
    clf = GradientBoostingClassifier()
    scores = cross_val_score(clf, X, y_bin, cv=3)
    print 'Classification by gradient boosting score: ', scores.mean()


     # REGRESSION

    print('\nRegression by random forest for the Box Office...')
    reg = RandomForestRegressor()
    scores = cross_val_score(reg, X, y, cv=3)
    print 'Regression by random forest score: ', scores.mean()

    print('\nRegression by gradient boosting for the Box Office...')
    reg = GradientBoostingRegressor()
    scores = cross_val_score(reg, X, y, cv=3)
    print 'Regression by gradient boosting score: ', scores.mean()

def BoxOfficePlot():
    fig = plt.figure()

    fig.suptitle(u'Box Office prédit en fonction du box office réel')

    ax = fig.add_subplot(111)
    ax.set_xlabel(u'Log du box office réel')
    ax.set_ylabel(u'Log du box office prédit')
    ax.set_xlim([0,30])
    ax.set_ylim([0,30])

    y = app.predict_labels_log_box_office.ravel()
    reg = RandomForestRegressor()
    reg.fit(X[0::2],y[0::2])

    ax.plot(y[1::2], reg.predict(X[1::2]), '+')
    plt.show()


###############
### Reviews ###
###############

def ReviewsScores():
    Y = app.predict_labels_reviews
    RF_clf = []
    RF_clf_scores = []
    GB_clf = []
    GB_clf_scores = []
    RF_reg = []
    RF_reg_scores = []
    GB_reg = []
    GB_reg_scores = []
   
    print "Number of Journals: ", app.nb_journals

    for i in range(app.nb_journals):
        y = Y[:,i]
        y_bin = y > np.median(y)

        RF_clf.append(RandomForestClassifier())
        GB_clf.append(GradientBoostingClassifier())
        RF_reg.append(RandomForestRegressor())
        GB_reg.append(GradientBoostingRegressor())

        RF_clf_scores.append(cross_val_score(RF_clf[i], X, y_bin, cv=3).mean())
        print "Journal ", i, " - ", "Reviews classification by random forest score: ", RF_clf_scores[i]
        GB_clf_scores.append(cross_val_score(GB_clf[i], X, y_bin, cv=3).mean())
        print "Journal ", i, " - ", "Reviews classification by gradient boosting score: ", GB_clf_scores[i]
        RF_reg_scores.append(cross_val_score(RF_reg[i], X, y, cv=3).mean())
        print "Journal ", i, " - ", "Reviews regression by random forest score: ", RF_reg_scores[i]
        GB_reg_scores.append(cross_val_score(GB_reg[i], X, y, cv=3).mean())
        print "Journal ", i, " - ", "Reviews regression by gradient boosting score: ", GB_reg_scores[i]

    print   "Reviews classification by random forest score: ", RF_clf_scores.mean()
    print   "Reviews classification by gradient boosting score: ", GB_clf_scores.mean()
    print   "Reviews regression by random forest score: ", RF_reg_scores.mean()
    print   "Reviews regression by gradient boosting score: ", GB_reg_scores.mean()

###############
### Prizes ###
###############

def PrizesScores():
    Y = app.predict_labels_prizes
    RF_clf = []
    RF_clf_scores = []
    GB_clf = []
    GB_clf_scores = []
    RF_reg = []
    RF_reg_scores = []
    GB_reg = []
    GB_reg_scores = []
    LG_reg = []
    LG_reg_scores = []
    
    print "Number of Prizes: ", app.nb_considered_prizes

    for i in range(app.nb_considered_prizes):
        y = Y[:,i]
        y_bin = y > np.median(y)

        RF_clf.append(RandomForestClassifier())
        GB_clf.append(GradientBoostingClassifier())
        RF_reg.append(RandomForestRegressor())
        GB_reg.append(GradientBoostingRegressor())
        LG_reg.append(LogisticRegression())

        RF_clf_scores.append(cross_val_score(RF_clf[i], X, y_bin, cv=3).mean())
        print "Institution ", i, " - ", "Prizes classification by random forest score: ", RF_clf_scores[i]
        GB_clf_scores.append(cross_val_score(GB_clf[i], X, y_bin, cv=3).mean())
        print "Institution ", i, " - ", "Prizes classification by gradient boosting score: ", GB_clf_scores[i]
        RF_reg_scores.append(cross_val_score(RF_reg[i], X, y, cv=3).mean())
        print "Institution ", i, " - ", "Prizes regression by random forest score: ", RF_reg_scores[i]
        GB_reg_scores.append(cross_val_score(GB_reg[i], X, y, cv=3).mean())
        print "Institution ", i, " - ", "Prizes regression by gradient boosting score: ", GB_reg_scores[i]
        LG_reg_scores.append(cross_val_score(LG_reg[i], X, y, cv=3).mean())
        print "Institution ", i, " - ", "Prizes regression by logistic regression score: ", LG_reg_scores[i]

    print   "Prizes classification by random forest score: ", RF_clf_scores.mean()
    print   "Prizes classification by gradient boosting score: ", GB_clf_scores.mean()
    print   "Prizes regression by random forest score: ", RF_reg_scores.mean()
    print   "Prizes regression by gradient boosting score: ", GB_reg_scores.mean()
    print   "Prizes regression by logistic regression score: ", LG_reg_scores.mean()

#BoxOfficeScores()
#ReviewsScores()
#PrizesScores()

BoxOfficePlot()
