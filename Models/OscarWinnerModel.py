from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score


class OscarWinnerModel:
    def __init__(self, train_df, test_df):
        self.train_df = train_df

        self.test_df = test_df

    def train_test(self):
        # Extract features and target variable from the training set
        X_train = self.train_df.drop('Oscar Winners', axis=1)
        y_train = self.train_df['Oscar Winners']

        # Extract features and target variable from the test set
        X_test = self.test_df[X_train.columns]
        y_test = self.test_df['Oscar Winners']

        # Train the model
        # model = LogisticRegression(max_iter=1500)
        # model = SVC(kernel='linear')
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        self.test_df['Predicted Oscar Winners'] = y_pred

        # Save the DataFrame back to the Excel file with predictions
        self.test_df.to_excel('Data/movies_test.xlsx', index=False)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'\nAccuracy: {accuracy}')

        # Classification Report
        print('\nClassification Report:\n', classification_report(y_test, y_pred, zero_division=1))

        cv_accuracy = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        print(f'\nCross-Validation Accuracy: {cv_accuracy.mean()}')

        # Print the predictions
        print("\nPredictions for 'Oscar Winners':", y_pred)
