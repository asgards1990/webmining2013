# -*- coding: utf-8 -*-

# Obtenir le contraste et la luminosité d'une image

import Image, ImageStat     # besoin d'installer le module PIL
from operator import itemgetter

plt = Image.open("palette.bmp")  # ouvrir la palette au format .bmp

im = Image.open("image.jpg")    # ouvrir l'image
stat = ImageStat.Stat(im.convert('L'))  # convertir en niveaux de gris et instancier les stats

contraste = stat.stddev[0]  # le contraste correspond à l'écart-type...
luminosite = stat.mean[0]   # et la luminosité à la moyenne

# Trouver la couleur la plus fréquente dans une palette donnee

converted = im.quantize(palette = plt)
    # convertir l'image selon cette palette (palette facile à créer avec Photoshop)

dominant_colour = max(converted.getcolors(), key = itemgetter(0))[1]
    # trouver la couleur la plus fréquente

# Le script met environ 1 minute à s'exécuter pour 10 000 itérations