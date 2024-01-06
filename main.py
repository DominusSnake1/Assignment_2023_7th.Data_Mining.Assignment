import os
import pandas as pd
from Other import Utils
from Classes.Preprocessing import ProcessColumns
from Models.OscarWinnerModel import OscarWinnerModel


def main():
    # Initialize or load the dataset based on user input.
    demo_num, dataset = Utils.startup()

    # Process the Train Dataset.
    if not os.path.exists('Data/movies_train.xlsx'):
        ProcessColumns.processTrainSet(dataset)

    # If a demo file was created, remove it.
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")

    # Process the Test Dataset.
    if not os.path.exists('Data/movies_test.xlsx'):
        ProcessColumns.processTestSet()

    train_df = pd.read_excel('Data/movies_train.xlsx')
    test_df = pd.read_excel('Data/movies_test.xlsx')

    if os.path.exists("Data/predictions.csv"):
        os.remove("Data/predictions.csv")

    model = OscarWinnerModel(train_df, test_df)
    model.train_test()


if __name__ == '__main__':
    main()
