from cinema.models import *
import numpy as np

def getAvgGrade(genre):
	films=[]
	for film in Film.objects.all():
		genres = film.genres.all()
		if genre in genres:
			films.append(film)
	if films == []:
		return None
	grades=[]
	for film in films:
		reviews = Review.objects.filter(film=film).all()
		local_grades = []
		for review in reviews:
			local_grades.append(review.grade)
		if local_grades !=[]:
			grades.append(np.mean(local_grades))
	if grades == []:
		return None
	return np.mean(grades)

def printAvgGradeByGenre():
	for genre in Genre.objects.all():
		avg_grade = getAvgGrade(genre)
		if avg_grade == None:
			print(genre.name + ' : No film in database, or no reviews.')
			continue
		print(genre.name + ' : ' + str(getAvgGrade(genre)))
	
def checkImdbInfo():
	nb_films = Film.objects.all().count()
	nb_films_no_info = Film.objects.filter(imdb_user_rating=None,imdb_nb_user_ratings=None,imdb_nb_user_reviews=None,imdb_nb_reviews=None).all().count()
	nb_films_all_info = Film.objects.exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(imdb_nb_user_reviews=None).exclude(imdb_nb_reviews=None).all().count()
	nb_films_all_info_except_nbreviews = Film.objects.exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(imdb_nb_user_reviews=None).all().count()
	nb_films_all_rating_info = Film.objects.exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).all().count()
	print('Nb of films in DB : '+str(nb_films))
	print('Nb of films with no Imdb rating info : '+str(nb_films_no_info))
	print('Nb of films wtih all Imdb rating info : '+str(nb_films_all_info))
	print('Nb of films wtih info rating, nb_raters, nb_user_reviews : '+str(nb_films_all_info_except_nbreviews))
	print('Nb of films wtih info rating, nb_raters : '+str(nb_films_all_rating_info))

def statsBudgetBOMetacritic():
	films = Film.objects.exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None).exclude(imdb_nb_user_reviews=None).exclude(imdb_nb_reviews=None)
	films_wo_budget = films.filter(budget=None)
	films_wo_budget_bo = films_wo_budget.filter(box_office=None)
	films_wo_bo = films.filter(box_office=None)
	films_wo_metacritic = films.filter(metacritic_score=None)
	films_wo_metacritic_bo = films_wo_metacritic.filter(box_office=None)
	films_wo_metacritic_budget = films_wo_metacritic.filter(budget=None)
	films_wo_metacritic_budget_bo = films_wo_metacritic_budget.filter(box_office=None)
	print('Nb of films : '+str(films.count()))
	print('Nb of films without budget : '+str(films_wo_bo.count()))
	print('Nb of films without box-office : '+str(films_wo_budget.count()))
	print('Nb of films without metacritic : '+str(films_wo_metacritic.count()))
	print('Nb of films without (budget,box-office) : '+str(films_wo_budget_bo.count()))
	print('Nb of films without (metacritic,box-office) : '+str(films_wo_metacritic_bo.count()))
	print('Nb of films without (metacritic,budget) : '+str(films_wo_metacritic_budget.count()))
	print('Nb of films without (metacritic,budget,box-office) : '+str(films_wo_metacritic_budget_bo.count()))
	print('Nb of films with budget only : '+str(films_wo_metacritic_bo.exclude(budget=None).count()))
	print('Nb of films with box-office only : '+str(films_wo_metacritic_budget.exclude(box_office=None).count()))
	print('Nb of films with metacritic only : '+str(films_wo_budget_bo.exclude(metacritic_score=None).count()))

def filterFilms():
	print('Nb of films in DB : ' + str(Film.objects.count()))
	films = Film.objects.exclude(runtime=None).exclude(genres=None).exclude(country=None).exclude(imdb_user_rating=None).exclude(imdb_nb_user_ratings=None)
	for film in films:
		if film.imdb_nb_user_reviews==None:
			film.imdb_nb_user_reviews=0
		if film.imdb_nb_reviews==None:
			film.imdb_nb_reviews=0
	print('Nb of films after cleaning : ' + str(films.count()) + '. Selected ' + str(float(films.count())/Film.objects.count()) + ' %.')