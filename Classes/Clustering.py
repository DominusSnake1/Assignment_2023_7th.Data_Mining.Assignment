from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from icecream import ic
import pandas as pd


def clustering(train_df):
    X = train_df.drop('Oscar Winners', axis=1)

    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(X)

    clusters_num = 2

    # KMeans
    # kmeans_elbow_silhouette(reduced_features)
    kmeans_plot(clusters=clusters_num, features=reduced_features)

    # DBSCAN
    dbscan_plot(features=reduced_features)

    # Hierarchical
    hierarchical_plot(clusters=clusters_num, features=reduced_features)


def kmeans_elbow_silhouette(features):
    distortions = []
    silhouette_scores = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(features)
        labels = kmeans.labels_
        distortions.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(features, labels))

    figure = plt.figure()

    figure.add_subplot(1, 2, 1)
    plt.plot(distortions, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')

    figure.add_subplot(1, 2, 2)
    plt.plot(silhouette_scores, marker='o')
    plt.title('Silhouette Score')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')

    plt.show()


def kmeans_plot(clusters, features):
    kmeans = KMeans(n_clusters=clusters, random_state=42)
    labels = kmeans.fit_predict(features)

    plt.scatter(features[:, 0], features[:, 1], c=labels)
    plt.title('KMeans')
    plt.show()

    silhouette_avg = silhouette_score(features, labels)
    print(f'Silhouette Score: {silhouette_avg}')

    features_labeled = pd.DataFrame({'Feature 1': features[:, 0], 'Feature 2': features[:, 1], 'Cluster': labels})

    cluster_descriptions = features_labeled.groupby('Cluster').mean()
    print(cluster_descriptions)


def dbscan_plot(features):
    dbscan = DBSCAN(eps=0.15, min_samples=12)
    labels = dbscan.fit_predict(features)

    plt.scatter(features[:, 0], features[:, 1], c=labels)
    plt.title('DBScan')
    plt.show()

    silhouette_avg = silhouette_score(features, labels)
    print(f'Silhouette Score: {silhouette_avg}')

    features_labeled = pd.DataFrame({'Feature 1': features[:, 0], 'Feature 2': features[:, 1], 'Cluster': labels})

    cluster_descriptions = features_labeled.groupby('Cluster').mean()
    print(cluster_descriptions)


def hierarchical_plot(clusters, features):
    hc = AgglomerativeClustering(n_clusters=clusters, linkage='ward')
    hc.fit(features)
    labels = hc.labels_

    plt.scatter(features[:, 0], features[:, 1], c=labels)
    plt.title('Hierarchical')
    plt.show()
