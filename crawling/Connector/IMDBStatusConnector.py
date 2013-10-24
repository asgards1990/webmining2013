# /usr/bin/env python
# -*- coding: utf-8 -*-


####################################################################


#importe les modules internes
import Logger.init_logger as initLogger #Initialise le logger
import Logger.logger_config as loggerConfig

import connector_config as ConnectorConfig

from status.models import IMDBFilmStatus

####################################################################

class IMDBFilmStatusConnector:
     
    def __init__(self):
        self.logger = initLogger.getLogger(ConnectorConfig.IMDB_STATUS_CONNECTOR_LOGGER_NAME)
    
    ###############################################################################

    def id_exists(self, imdb_id):
        self.logger.debug("Find if the IMDB ID {} exists in the database:".format(imdb_id))
        
        try:
            s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        except IMDBFilmStatus.DoesNotExist:
            self.logger.debug("-> IMDB ID {} does not exist in the database".format(imdb_id))
            return False
        else:
            self.logger.debug("-> IMDB ID {} exists in the database".format(imdb_id))
            return True

    def insert(self, imdb_id, year, position):
        self.logger.debug("Insert film status (imdb_id={0}, year={1}, position={2}) into the database (if not exists)".format(imdb_id, year, position))
        
        if not self.id_exists(imdb_id):
            film_status = IMDBFilmStatus(imdb_id=imdb_id, year=year, position=position,
                                         film_mainpage=0, film_fullcredits=0, film_awards=0, film_reviews=0, film_keywords=0, film_companycredits=0,
                                         film_image=0,
                                         downloaded=0, extracted=0)
            try:
                film_status.save()
            except Exception as e:
                self.logger.warning("-> The film status couldn't be inserted into the database:")
                self.logger.warning("-> Error: {}".format(e))
                return False
            else:
                self.logger.debug("-> Film status inserted into the database")
                return True
        else:
            self.logger.warning("-> The film status couldn't be inserted because it already exists in the database")
            return False

    def delete(self, imdb_id):
        self.logger.debug("Delete film status for IMDB ID {} from the database:".format(imdb_id))

        try:
            s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
            s.delete()
        except Exception as e:
            self.logger.warning("-> Film status for IMDB ID {} couldn't be deleted from the database".format(imdb_id))
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status for IMDB ID {} deleted from the database".format(imdb_id))
            return True
    
    ###############################################################################

    # GET METHODS

    def getFilmMainPageStatus(self, imdb_id):
        self.logger.debug("Get the film Main Page status for IMDB ID {} in the database:".format(imdb_id))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        status = s.film_mainpage
        
        self.logger.debug("-> Status: {}".format(status))
        return status

    def getFilmFullCreditsStatus(self, imdb_id):
        self.logger.debug("Get the film Full Credits status for IMDB ID {} in the database:".format(imdb_id))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        status = s.film_fullcredits

        self.logger.debug("-> Status: {}".format(status))
        return status

    def getFilmAwardsStatus(self, imdb_id):
        self.logger.debug("Get the film Awards status for IMDB ID {} in the database:".format(imdb_id))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        status = s.film_awards
        
        self.logger.debug("-> Status: {}".format(status))
        return status

    def getFilmReviewsStatus(self, imdb_id):
        self.logger.debug("Get the film Reviews status for IMDB ID {} in the database:".format(imdb_id))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        status = s.film_reviews
        
        self.logger.debug("-> Status: {}".format(status))
        return status

    def getFilmKeywordsStatus(self, imdb_id):
        self.logger.debug("Get the film Keywords status for IMDB ID {} in the database:".format(imdb_id))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        status = s.film_keywords
        
        self.logger.debug("-> Status: {}".format(status))
        return status

    def getFilmCompanyCreditsStatus(self, imdb_id):
        self.logger.debug("Get the film Company Credits status for IMDB ID {} in the database:".format(imdb_id))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        status = s.film_companycredits
        
        self.logger.debug("-> Status: {}".format(status))
        return status

    def getNotDownloaded(self):
        self.logger.debug("Get the IMDB ID {} in the database with downloaded")
        
        status = IMDBFilmStatus.objects.filter(downloaded=0)
        return map(lambda s: s.imdb_id, status)

    ###############################################################################

    # SET METHODS

    def setFilmMainPageStatus(self, imdb_id, status):
        self.logger.debug("Set the film Main Page status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.film_mainpage = status
        
        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True


    def setFilmFullCreditsStatus(self, imdb_id, status):
        self.logger.debug("Set the film Full Credits status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.film_fullcredits = status

        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True

    def setFilmAwardsStatus(self, imdb_id, status):
        self.logger.debug("Set the film Awards status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.film_awards = status

        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True

    def setFilmReviewsStatus(self, imdb_id, status):
        self.logger.debug("Set the film Reviews status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.film_reviews = status

        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True

    def setFilmKeywordsStatus(self, imdb_id, status):
        self.logger.debug("Set the film Keywords status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.film_keywords = status

        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True

    def setFilmCompanyCreditsStatus(self, imdb_id, status):
        self.logger.debug("Set the film Company Credits status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.film_companycredits = status

        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True

    def setDownloadedStatus(self, imdb_id, status):
        self.logger.debug("Set the Downloaded status for IMDB ID {0} to {1} in the database".format(imdb_id, status))
        
        s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        s.downloaded = status

        try:
            s.save()
        except Exception as e:
            self.logger.warning("-> The film status couldn't be saved")
            self.logger.warning("-> Error: {}".format(e))
            return False
        else:
            self.logger.debug("-> Film status modified")
            return True

####################################################################


