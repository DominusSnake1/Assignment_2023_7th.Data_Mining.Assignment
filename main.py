from Models.OscarWinnerModel import OscarWinnerModel
from Classes.Clustering import clustering
from Other import Utils, Metrics
import pandas as pd


def main():
    # Initialize or load the dataset based on user input.
    demo_num, dataset = Utils.startup()

    Utils.check_if_files_exist(
        dataset=dataset,
        demo_num=demo_num
    )

    train_df = pd.read_excel('Data/movies_train.xlsx')
    Metrics.test_training(train_df)

    test_df = pd.read_excel('Data/movies_test.xlsx')
    model = OscarWinnerModel(train_df, test_df)
    model.train()

    clustering(train_df)


if __name__ == '__main__':
    main()
