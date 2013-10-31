import sklearn
from sklearn.preprocessing import Imputer # manage missing values
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

def getRandomForestRegressorCVScore(X,y):
    imputer = Imputer(missing_values=-1)
    clf_class = RandomForestRegressor()
    pipeline_class = Pipeline([('imputer', imputer), ('clf', clf_class)])
    return cross_val_score(pipeline_class, X, y, cv=3)
