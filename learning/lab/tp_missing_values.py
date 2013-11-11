import service.prodbox
import scipy
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier,GradientBoostingRegressor
from sklearn import cross_validation

app = service.prodbox.CinemaService()

X = scipy.sparse.hstack([
        app.imdb_user_rating_matrix,
        app.imdb_nb_user_ratings_matrix,
        app.languages_matrix,
        app.genres_matrix]).toarray()

# Box office
y = app.box_office_matrix.toarray()[:,0]
nan_indexes = np.isnan(y)

#reg = RandomForestRegressor(n_jobs=-1)
reg = GradientBoostingRegressor()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X[-nan_indexes, :], y[-nan_indexes], test_size=0.2, random_state=0)

reg.fit(X_train, y_train)
print('Score: ' + str(reg.score(X_test, y_test)) )

y[nan_indexes] = reg.predict(X[nan_indexes, :])
