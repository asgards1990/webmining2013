import sklearn
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

def getRandomForestClassifierCVScore(X,y,completer):
    clf_class = RandomForestClassifier()
    pipeline_class = Pipeline([('completer', completer), ('clf', clf_class)])
    clf_class.fit(X, y)
    fi = clf_class.feature_importances_
    print (fi.argsort()[-5:]) # The 5 most important features
    return cross_val_score(pipeline_class, X, y, cv=3)
