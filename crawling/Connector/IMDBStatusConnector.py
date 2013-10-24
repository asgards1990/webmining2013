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
     
    def id_exists(self, imdb_id):
        self.logger.debug("Find if the IMDB ID {} exists in the database".format(imdb_id))
        
        try:
            s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
        except IMDBFilmStatus.DoesNotExist:
            self.logger.debug("IMDB ID {} does not exist in the database".format(imdb_id))
            return False
        else:
            self.logger.debug("IMDB ID {} exists in the database".format(imdb_id))
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
                self.logger.warning("The film status couldn't be inserted into the database")
                self.logger.warning("Error: {}".format(e))
                return False
            else:
                self.logger.debug("Film status inserted into the database")
                return True
        else:
            self.logger.warning("The film status couldn't be inserted because it already exists in the database")
            return False

    def delete(self, imdb_id):
        self.logger.debug("Delete film status for IMDB ID {} from the database".format(imdb_id))

        try:
            s = IMDBFilmStatus.objects.get(imdb_id=imdb_id)
            s.delete()
        except Exception as e:
            self.logger.warning("Film status for IMDB ID {} couldn't be deleted from the database".format(imdb_id))
            self.logger.warning("Error: {}".format(e))
            return False
        else:
            self.logger.debug("Film status for IMDB ID {} deleted from the database".format(imdb_id))
            return True


####################################################################


