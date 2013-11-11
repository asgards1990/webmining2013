import service.prodbox
from sklearn.manifold import SpectralEmbedding, spectral_embedding_
from sklearn.cluster import SpectralClustering
from sklearn.utils.sparsetools import connected_components
from sklearn.neighbors import kneighbors_graph
from sklearn.utils.graph import graph_laplacian
import numpy as np
from sklearn.utils.arpack import eigsh

app = service.prodbox.CinemaService()

X = app.getWeightedSearchFeatures(15)

graph = kneighbors_graph(X, 10)
lap = graph_laplacian(graph, True)

from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components = 30, algorithm="arpack")
lap = spectral_embedding_._set_diag(lap, 1)
svd.fit(-lap)

eigenvalues = np.diag(svd.components_ * (-lap).todense() * svd.components_.T)

eigenvalues2, _ = eigsh(-lap, k=30, which='LM', sigma=1)
print(eigenvalues)

print(eigenvalues2)

se = SpectralEmbedding(n_components = 30, eigen_solver='arpack', affinity="nearest_neighbors")
se.fit(X)

app.quit()

# TODO : check budget distribution, draw budget conditionnaly
out = connected_components(graph)

