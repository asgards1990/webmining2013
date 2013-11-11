import sklearn
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

def getRandomForestRegressorCVScore(X,y,completer):
    clf_class = RandomForestRegressor()
    pipeline_class = Pipeline([('completer', completer), ('clf', clf_class)])
    return cross_val_score(pipeline_class, X, y, cv=3)


def getGradientBoostingRegressorCVScore(X,y,completer):
    clf_class = GradientBoostingRegressor()
    pipeline_class = Pipeline([('completer', completer), ('clf', clf_class)])
    return cross_val_score(pipeline_class, X, y, cv=3)
