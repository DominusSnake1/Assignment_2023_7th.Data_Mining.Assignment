from Other.Utils import algorithm_selector
import pandas as pd
import numpy as np


def statistics(y_test, y_pred):
    from sklearn.metrics import accuracy_score, classification_report, f1_score
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

    print('Classification Report:\n', classification_report(y_test, y_pred, zero_division=1))

    num_winners = sum(1 if x == 1 else 0 for x in y_pred)
    print(f"Number of 'Predicted' Winners: {num_winners}")

    f1 = f1_score(y_test, y_pred)
    print(f'F1-Score: {f1}')


class OscarWinnerModel:
    """
        The class representing the Oscar Winner prediction model.

        :param train_df: The training dataset.
        :param test_df: The testing dataset.
    """

    def __init__(self, train_df, test_df):
        """
            The method initializes the OscarWinnerModel instance.

            :param train_df: The training dataset.
            :param test_df: The testing dataset.
        """
        self.train_df = train_df
        self.test_df = test_df

        # Extract features and target variable from the training set
        self.X_train = train_df[test_df.columns].drop('Oscar Winners', axis=1)
        self.y_train = train_df['Oscar Winners']

        # Extract features and target variable from the test set
        self.X_test = test_df[self.X_train.columns]
        self.y_test = test_df['Oscar Winners']

    def train_test(self):
        """
            The method trains the model and performs predictions on the test set.\n
            It uses the selected algorithm to train the model, make predictions and to evaluate performance using accuracy, classification report,
            cross-validation accuracy, and the number of predicted winners.
         """
        # Train the model
        model = None
        algorithm = algorithm_selector()

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

        model.fit(self.X_train, self.y_train)

        # Get the top 11 predictions with a higher chance of being an Oscar Winner.
        y_proba = model.predict_proba(self.X_test)
        winner_probabilities = y_proba[:, 1]

        top_11_predictions = winner_probabilities.argsort()[-11:]
        y_pred = np.zeros_like(winner_probabilities, dtype=int)
        y_pred[top_11_predictions] = 1

        # Create the new Dataframe with the predictions.
        pred_df = pd.DataFrame()
        pred_df['ID'] = self.test_df['ID']
        pred_df['OSCAR'] = y_pred

        # Save the DataFrame back to the Excel file with predictions
        pred_df.to_csv('Data/predictions.csv', index=False)

        # Statistics
        statistics(self.y_test, y_pred)
