import numpy as np
from service.vectorizers import *
from sklearn import linear_model

films = Film.objects.order_by('-release_date').all()

X_budget = getBudgetFeatures(films)
Y = getBoxOfficeFeatures(films)

index = (X_budget[:, 1] == 0) * (-np.isnan(Y[:,0]))

Xp = asmatrix(X_budget[index, 0])
Yp = Y[index]


clf = linear_model.LinearRegression()
clf.fit(transpose(Xp), Yp)
clf.coef_

# Explained variance score
clf.score(transpose(Xp), Yp)

res = clf.predict(transpose(Xp)) - Yp
hist(res, bins=30)
# le predicteur lineaire surestime le box office en fonction du budget

clf2 = linear_model.LinearRegression()
clf2.fit(transpose(log(Xp)), log(Yp))
res = clf.predict(transpose(Xp)) - Yp
clf2.score(transpose(Xp), Yp)
# meilleur score en log, log

# etude par saison