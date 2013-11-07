import numpy as np
import service.prodbox as pb
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier ,RandomForestRegressor
from sklearn.cross_validation import cross_val_score
import copy


app=pb.CinemaService()

X=app.predict_features
y=app.predict_labels			                                     #y=app.box_office_matrix.toarray().ravel() 

yr=[]
review_gradient_boosting_reg=[]
review_random_forest_reg=[]
scores_random_forest=[]
scores_gradient_boosting=[]

for i in range(len(app.reviews_names)):
	yr.append(y[:,1+i])                                                  #yr.append(app.reviews_matrix[:,i].toarray())
	review_gradient_boosting_reg.append(GradientBoostingRegressor())
	review_random_forest_reg.append(RandomForestRegressor())
	review_gradient_boosting_reg[i].fit(X, yr[i])
	review_random_forest_reg[i].fit(X, yr[i])
	scores_gradient_boosting.append(cross_val_score(review_gradient_boosting_reg[i], X, yr[i], cv=3).mean())
	scores_random_forest.append(cross_val_score(review_random_forest_reg[i], X, yr[i], cv=3).mean())

print   "scores reviews Random Forest=",scores_random_forest
print 	"scores reviews Gradient Boosting=",scores_gradient_boosting







ybo=y[:,0]
y_log = np.log(ybo)


yy=copy.deepcopy(ybo) # on va trier yy, on a besoin d'une copie pour ne pas trier ybo
yy.sort()
yy_log=np.log(yy)
yy_log=yy_log[::1]

a=range(len(yy_log))

px=np.poly1d(np.polyfit(a,yy_log,1))

z=np.poly1d(np.polyfit(yy_log,px(a),10))  # la fonction z linearise y_log
					   #pour calculer son inverse, soit fsolve, soit np.poly1d(np.polyfit(px(a),yy_log,10))  (ie on change 						   #l'abscisse et l'ordonnee)
					
y_pol=z(y_log)
y_bin = y_log > np.median(y_log)
y_pol_bin= y_pol > np.median(y_pol)




# CLASSIFICATION
print('\nClassification by random forest for the Box Office...')
        
           
clf = RandomForestClassifier()

scores = cross_val_score(clf, X, y_bin, cv=3)
print 'Classification by random forest score : ', scores.mean()

scores = cross_val_score(clf, X, y_pol_bin, cv=3)
print 'Classification by random forest score with y_pol : ', scores.mean()




print('\nClassification by gradient boosting for the Box Office...')
clf = GradientBoostingClassifier()
        
scores = cross_val_score(clf, X, y_bin, cv=3)
print 'Classification by gradient boosting score : ', scores.mean()

scores = cross_val_score(clf, X, y_pol_bin, cv=3)
print 'Classification by gradient boosting score with y_pol : ', scores.mean()


 # REGRESSION

print('\nRegression by random forest for the Box Office...')
clf = RandomForestRegressor()
        
scores = cross_val_score(clf, X, y_log, cv=3)
print 'Regression by random forest score : ', scores.mean()
       
scores = cross_val_score(clf, X, y_pol, cv=3)
print 'Regression by random forest score with y_pol : ', scores.mean()

###
print('\nRegression by gradient boosting for the Box Office...')
clf = GradientBoostingRegressor()
        
scores = cross_val_score(clf, X, y_log, cv=3)
print 'Regression by gradient boosting score : ', scores.mean()
       
scores = cross_val_score(clf, X, y_pol, cv=3)
print 'Regression by gradient boosting score with y_pol : ', scores.mean()


#app.quit()
