import prodbox as pb
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import cross_val_score
import numpy as np

def RandomForestBoxOfficeBenchmark():
    app = pb.CinemaService()

    X = app.predict_features.toarray()
    feature_names = app.predict_features_names
    
    y = app.predict_labels.toarray()

    ##################
    ### BOX OFFICE ###
    ##################

    y = y[:,0]
    y_log = np.log(y)
    
    # CLASSIFICATION
    print('\nRandom Forest classification for the Box Office...')
    
    thresh = np.median(y_log)
    y_bin = y_log > thresh
    
    clf = RandomForestClassifier()
    
    scores = cross_val_score(clf, X, y_bin, cv=3)
    print 'Classification score : ', scores.mean()
    
    clf.fit(X, y_bin)
    fi = clf.feature_importances_
    fi_indexes = fi.argsort()[-5:] # The 5 most important features
    i=1
    for index in reversed(fi_indexes):
        print(str(i)+'th component : '+feature_names[index]+' with weight '+str(fi[index]))
        i=i+1
    
    # REGRESSION
    print('\nRandom Forest regression...')
    clf = RandomForestRegressor()
    
    scores = cross_val_score(clf, X, y_log, cv=3)
    print 'Classification score : ', scores.mean()
    
    clf.fit(X, y_log)
    fi = clf.feature_importances_
    fi_indexes = fi.argsort()[-5:] # The 5 most important features
    i=1
    for index in reversed(fi_indexes):
        print(str(i)+'th component : '+feature_names[index]+' with weight '+str(fi[index]))
        i=i+1

