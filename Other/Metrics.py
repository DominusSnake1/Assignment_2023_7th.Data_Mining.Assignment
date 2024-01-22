from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

from Other.Utils import algorithm_selector


def test_training(dataset):
    algorithm = algorithm_selector()

    X = dataset.drop('Oscar Winners', axis=1)
    y = dataset['Oscar Winners']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.5,
        random_state=42
    )

    model = None

    if algorithm == 'LR':
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression(max_iter=1500)
    elif algorithm == 'DTC':
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()
    elif algorithm == 'RFC':
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier()
    elif algorithm == 'KNN':
        from sklearn.neighbors import KNeighborsClassifier
        model = KNeighborsClassifier(n_neighbors=3)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("=====[ Training Statistics ]=====")
    statistics(algorithm, y_test, y_pred)


def statistics(algorithm, y_test, y_pred):
    print(f"Algorithm used: {algorithm}\n")

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}\n')

    print('Classification Report:\n', classification_report(
        y_test,
        y_pred,
        zero_division=1)
    )

    f1 = f1_score(y_test, y_pred)
    print(f'F1-Score: {f1}')
