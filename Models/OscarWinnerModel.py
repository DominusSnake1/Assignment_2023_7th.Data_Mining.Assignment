import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


class OscarWinnerModel:
    def __init__(self):
        # Load train dataset.
        train_df = pd.read_excel('Data/movies_train.xlsx')
        self.train_df = train_df

        # Load test dataset.
        test_df = pd.read_excel('Data/movies_test.xlsx')
        self.test_df = test_df

    def train_test(self):
        X_train = self.train_df.drop('Oscar Winners', axis=1)
        y_train = self.train_df['Oscar Winners']

        X_test = self.test_df[X_train.columns]
        y_test = self.test_df['Oscar Winners']

        model = LogisticRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')

        # Classification Report
        print('Classification Report:\n', classification_report(y_test, y_pred))

        from sklearn.model_selection import cross_val_score
        cv_accuracy = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        print(f'Cross-Validation Accuracy: {cv_accuracy.mean()}')
