from django.db import models

# Model for IMDB status
class IMDBstatus(models.Model):
    imdb_id = models.CharField(max_length=9)            # the IMDB identifier
    year = models.IntegerField()            # the release year
    position = models.IntegerField()        # the page in which the film appears
    # we need to download 5 webpages for each film
    film_page = models.IntegerField()       
    film_cast = models.IntegerField()
    film_awards = models.IntegerField()
    film_reviews = models.IntegerField()
    film_keywords = models.IntegerField()
    extracted = models.IntegerField()
    
    def save(self, *args, **kwargs):
        if len(self.imdb_id) != 9:
            raise Exception, "invalid IMDB id (its length should be 9)"
        elif self.year < 1950 or self.year > 2020:
            raise Exception, "the year should be between 1950 and 2020"
        elif self.position <= 0:
            raise Exception, "the position should be > 0"
        elif (self.film_page < 0 or self.film_page > 5) and self.film_page != 100:
            raise Exception, "the 'film_page' field should be between 0 and 5, or equal to 100"
        elif (self.film_cast < 0 or self.film_cast > 5) and self.film_cast != 100:
            raise Exception, "the 'film_cast' field should be between 0 and 5, or equal to 100"
        elif (self.film_awards < 0 or self.film_awards > 5) and self.film_awards != 100:
            raise Exception, "the 'film_awards' field should be between 0 and 5, or equal to 100"
        elif (self.film_reviews < 0 or self.film_reviews > 5) and self.film_reviews != 100:
            raise Exception, "the 'film_reviews' field should be between 0 and 5, or equal to 100"
        elif (self.film_keywords < 0 or self.film_keywords > 5) and self.film_keywords != 100:
            raise Exception, "the 'film_keywords' field should be between 0 and 5, or equal to 100"
        elif self.extracted < -1 or self.extracted > 1:
            raise Exception, "the 'extracted' field should be -1, 0 or 1"
        else:
            super(IMDBstatus, self).save(*args, **kwargs) # Call the "real" save() method.

