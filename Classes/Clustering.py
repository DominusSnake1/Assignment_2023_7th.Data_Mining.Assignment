from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd


def clustering(train_df) -> None:
    """
    The method performs clustering using KMeans, DBSCAN, and Agglomerate Clustering algorithms.

    :param train_df: DataFrame containing features and labels.
    """
    X = train_df.drop('Oscar Winners', axis=1)
    y = train_df['Oscar Winners']

    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(X)

    # KMeans
    print("\n==========[ KMeans ]==========")
    # plot_kmeans_elbow_silhouette(reduced_features)
    plot(title='KMEANS', x_axis=reduced_features, y_axis=y, clusters=2)

    # DBSCAN
    print("\n==========[ DBSCAN ]==========")
    plot(title='DBSCAN', x_axis=reduced_features, y_axis=y, eps=0.01, min_samples=3)

    # Hierarchical
    print("\n==========[ HAC ]==========")
    plot(title='HAC', x_axis=reduced_features, y_axis=y, clusters=2)


def plot(title, x_axis, y_axis, clusters=None, eps=None, min_samples=None) -> None:
    """
    The method plots the clusters formed by the clustering algorithms.

    :param title: The title of the plot.
    :param x_axis: The features to plot on the x-axis.
    :param y_axis: The labels for coloring the points.
    :param clusters: Number of clusters for KMeans and Agglomerate Clustering.
    :param eps: The maximum distance between two samples for DBSCAN.
    :param min_samples: The number of samples in a neighborhood for DBSCAN.
    """
    labels = None

    if title == 'KMEANS':
        kmeans = KMeans(n_clusters=clusters, random_state=42)
        labels = kmeans.fit_predict(x_axis)
    elif title == 'DBSCAN':
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(x_axis)
    elif title == 'HAC':
        hc = AgglomerativeClustering(n_clusters=clusters, linkage='ward')
        labels = hc.fit_predict(x_axis)

    plt.scatter(x_axis[:, 0], x_axis[:, 1], c=y_axis)
    plt.title(title)
    plt.show()

    compare_cluster_labels(y_axis, labels)

    show_avg_silhouette(x_axis, y_axis)

    show_cluster_description(x_axis, y_axis)


def show_avg_silhouette(x_axis, y_axis) -> None:
    """
    The method calculates and displays the average silhouette score.

    :param x_axis: The features used in clustering.
    :param y_axis: The labels used for clustering.
    """
    silhouette_avg = silhouette_score(x_axis, y_axis)
    print(f'Silhouette Score: {silhouette_avg}')


def show_cluster_description(x_axis, y_axis) -> None:
    """
    The method displays the cluster descriptions.

    :param x_axis: The features used in clustering.
    :param y_axis: The labels used for clustering.
    """
    features_labeled = pd.DataFrame({'Feature 1': x_axis[:, 0], 'Feature 2': x_axis[:, 1], 'Cluster': y_axis})

    cluster_descriptions = features_labeled.groupby('Cluster').mean()
    print(f"Cluster Description:\n{cluster_descriptions}")


def compare_cluster_labels(first_list, second_list) -> None:
    """
    The method compares the cluster labels with the ground truth labels.

    :param first_list: Ground truth labels.
    :param second_list: Cluster labels.
    """
    count_dict = {}

    for line, number in zip(first_list, second_list):
        if line == 1:
            count_dict[number] = count_dict.get(number, 0) + 1

    for number, count in count_dict.items():
        print(f"Cluster: {number} has {count} occurrences of `Oscar Winners`.")


def plot_kmeans_elbow_silhouette(features) -> None:
    """
    the method plots the elbow method and the silhouette score for KMeans.

    :param features: The features used for clustering.
    """
    distortions = []
    silhouette_scores = []

    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
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
