import service.prodbox
from sklearn.manifold import SpectralEmbedding
from sklearn.cluster import SpectralClustering
from sklearn.utils.sparsetools import connected_components

app = service.prodbox.CinemaService()

X = app.getWeightedSearchFeatures(15)

se = SpectralEmbedding(n_components = 10, eigen_solver='arpack', affinity="nearest_neighbors")

se.fit(X)