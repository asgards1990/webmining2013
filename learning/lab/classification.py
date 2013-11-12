import sklearn
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

def getRandomForestClassifierCVScore(X,y,completer):
    clf = RandomForestClassifier()
    pipeline = Pipeline([('completer', completer), ('clf', clf)])
    clf.fit(X, y)
    return (cross_val_score(pipeline, X, y, cv=3), clf.feature_importances_)
