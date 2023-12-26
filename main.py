import os
import pandas as pd
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset
from Models.OscarWinnerModel import OscarWinnerModel


def main():
    # Initialize or load the dataset based on user input.
    demo_num, dataset = startup()

    if not os.path.exists('Data/movies_train.xlsx'):
        # Process the Train Dataset.
        processTrainSet(dataset, demo_num)

    if os.path.exists('Data/movies_test.xlsx'):
        os.remove('Data/movies_test.xlsx')
        # Process the Test Dataset.
    processTestSet()

    train_df = pd.read_excel('Data/movies_train.xlsx')
    test_df = pd.read_excel('Data/movies_test.xlsx')
    train_df = train_df[test_df.columns]

    model = OscarWinnerModel(train_df, test_df)
    model.train_test()


def startup():
    """
    Function to determine whether to use a demo dataset or the complete dataset.

    :return: 1. Number of rows for the demo dataset.<br>
    2. Dataset object containing the original or a created demo dataset.
    """
    yn = input("Do you want to use a demo of the dataset? (y / [n])\n")

    if yn.lower() == "n":
        return None, Dataset()

    num = int(input("How many rows do you want in your demo?\n"))
    Dataset().createDEMO(num)
    return num, Dataset(f"Data/DEMO_{num}.xlsx")


def processTestSet(test_loc="Data/movies_test _anon_sample.xlsx"):
    """
    Processes the test dataset "movies_test _anon_sample.xlsx" into the processed Test Set "movies_test.xlsx"

    :param test_loc: The location of the Test Dataset.
    """
    df = Dataset(test_loc)
    pc = ProcessColumns(df)

    new_df = pc.addBlankColumn('Oscar Winners') \
        .processReleaseDate() \
        .processPrimaryGenre() \
        .processOneHotEncoder('Script Type', "SType") \
        .processOneHotEncoder('Primary Genre', "Genre") \
        .processMinMaxScaler('Rotten Tomatoes  critics') \
        .processMinMaxScaler('Rotten Tomatoes Audience ') \
        .processMinMaxScaler('Metacritic  critics') \
        .processMinMaxScaler('Metacritic Audience ') \
        .processMinMaxScaler('Average critics ') \
        .processMinMaxScaler('Average audience ') \
        .processMinMaxScaler('IMDb Rating') \
        .processMinMaxScaler('Opening weekend ($million)') \
        .processMinMaxScaler('Domestic gross ($million)') \
        .processMinMaxScaler('Foreign Gross ($million)') \
        .processMinMaxScaler('Worldwide Gross ($million)') \
        .processMinMaxScaler('Budget ($million)') \
        .processMinMaxScaler(' of Gross earned abroad', is_percentage=True) \
        .processMinMaxScaler(' Budget recovered', is_percentage=True) \
        .processMinMaxScaler(' Budget recovered opening weekend', is_percentage=True) \
        .processRatingDeviance('IMDB vs RT disparity',
                               'IMDb Rating',
                               'Rotten Tomatoes Audience ') \
        .processRatingDeviance('Rotten Tomatoes vs Metacritic  deviance',
                               'Rotten Tomatoes  critics',
                               'Metacritic  critics') \
        .processRatingDeviance('Audience vs Critics deviance ',
                               'Average audience ',
                               'Average critics ') \
        .dropColumn('Distributor') \
        .dropColumn('Opening Weekend') \
        .dropColumn('Domestic Gross') \
        .dropColumn('Foreign Gross') \
        .dropColumn('Worldwide Gross') \
        .dropColumn('Genre') \
        .dropColumn('Release Date (US)')\
        .dropColumn('Script Type')\
        .dropColumn('Primary Genre')\
        .dropColumn('Film')\
        .dropColumn('ID')

    processed_df = new_df.dataset

    # Save the processed dataset to a new Excel file.
    processed_df.to_excel('Data/movies_test.xlsx', index=False)
    print("Processed Dataframe (movies_test) is now created!\n")


def processTrainSet(df, demo_num):
    """
    Processes the original dataset "movies.xlsx" into the processed Train Set "movies_train.xlsx"

    :param df: Dataset object to be preprocessed.
    :param demo_num: Number of rows sampled in DEMO set.
    """
    if os.path.exists('Data/movies_train.xlsx'):
        return

    # Initialize ProcessColumns object for further processing.
    pc = ProcessColumns(df)

    # Generate IMDb data if not already present.
    if not os.path.exists('Data/imdb_data.xlsx'):
        pc.generateIMDbData()

    # Perform various data processing steps.
    new_df = pc.processIMDbRating() \
        .processOscarWinner() \
        .processReleaseDate() \
        .processPrimaryGenre() \
        .processOneHotEncoder('Script Type', "SType") \
        .processOneHotEncoder('Primary Genre', "Genre") \
        .processMinMaxScaler('Rotten Tomatoes  critics') \
        .processMinMaxScaler('Rotten Tomatoes Audience ') \
        .processMinMaxScaler('Metacritic  critics') \
        .processMinMaxScaler('Metacritic Audience ') \
        .processMinMaxScaler('Average critics ') \
        .processMinMaxScaler('Average audience ') \
        .processMinMaxScaler('IMDb Rating') \
        .processMinMaxScaler('Opening weekend ($million)') \
        .processMinMaxScaler('Domestic gross ($million)') \
        .processMinMaxScaler('Foreign Gross ($million)') \
        .processMinMaxScaler('Worldwide Gross ($million)') \
        .processMinMaxScaler('Budget ($million)') \
        .processMinMaxScaler(' of Gross earned abroad', is_percentage=True) \
        .processMinMaxScaler(' Budget recovered', is_percentage=True) \
        .processMinMaxScaler(' Budget recovered opening weekend', is_percentage=True) \
        .processRatingDeviance('IMDB vs RT disparity',
                               'IMDb Rating',
                               'Rotten Tomatoes Audience ') \
        .processRatingDeviance('Rotten Tomatoes vs Metacritic  deviance',
                               'Rotten Tomatoes  critics',
                               'Metacritic  critics') \
        .processRatingDeviance('Audience vs Critics deviance ',
                               'Average audience ',
                               'Average critics ') \
        .dropColumn('Distributor') \
        .dropColumn('Oscar Detail') \
        .dropColumn('Opening Weekend') \
        .dropColumn('Domestic Gross') \
        .dropColumn('Foreign Gross') \
        .dropColumn('Worldwide Gross') \
        .dropColumn('Genre') \
        .dropColumn('Release Date (US)')\
        .dropColumn('Script Type')\
        .dropColumn('Primary Genre')\
        .dropColumn('Film')

    processed_df = new_df.dataset

    # Save the processed dataset to a new Excel file.
    processed_df.to_excel('Data/movies_train.xlsx', index=False)
    print("Processed Dataframe (movies_test) is now created!\n")

    # If a demo file was created, remove it.
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")


if __name__ == '__main__':
    main()
