import pandas as pd
from Utils.Utils import algorithm_selector
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score


class OscarWinnerModel:
    def __init__(self, train_df, test_df):
        self.train_df = train_df
        self.test_df = test_df

    def train_test(self):
        # Extract features and target variable from the training set
        X_train = self.train_df[self.test_df.columns].drop('Oscar Winners', axis=1)
        y_train = self.train_df['Oscar Winners']

        # Extract features and target variable from the test set
        X_test = self.test_df[X_train.columns]
        y_test = self.test_df['Oscar Winners']

        # Train the model
        model = algorithm_selector()

        if model == 'LR':
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(max_iter=1500)
        elif model == 'DCT':
            from sklearn.tree import DecisionTreeClassifier
            model = DecisionTreeClassifier()
        elif model == 'RFC':
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier()
        elif model == 'KNN':
            from sklearn.neighbors import KNeighborsClassifier
            model = KNeighborsClassifier(n_neighbors=3)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        pred_df = pd.DataFrame()
        pred_df['ID'] = self.test_df['ID']
        pred_df['OSCAR'] = y_pred

        # Save the DataFrame back to the Excel file with predictions
        pred_df.to_csv('Data/predictions.csv', index=False)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')

        # Classification Report
        print('Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))

        cv_accuracy = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        print(f'Cross-Validation Accuracy: {cv_accuracy.mean()}')

        num_winners = sum(1 if x == 1 else 0 for x in y_pred)
        print(f"Number of 'Predicted' Winners: {num_winners}")
