import sklearn
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

def getRandomForestRegressorCVScore(X,y,completer):
    clf = RandomForestRegressor()
    pipeline = Pipeline([('completer', completer), ('clf', clf)])
    clf.fit(X, y)
    return (cross_val_score(pipeline, X, y, cv=3), clf.feature_importances_)
