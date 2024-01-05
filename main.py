import os
import pandas as pd
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset
from Models.OscarWinnerModel import OscarWinnerModel
from Utils import Utils


def main():
    # Initialize or load the dataset based on user input.
    demo_num, dataset = startup()

    # Process the Train Dataset.
    if not os.path.exists('Data/movies_train.xlsx'):
        processTrainSet(dataset)

    # If a demo file was created, remove it.
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")

    # Process the Test Dataset.
    if not os.path.exists('Data/movies_test.xlsx'):
        processTestSet()

    train_df = pd.read_excel('Data/movies_train.xlsx')
    test_df = pd.read_excel('Data/movies_test.xlsx')

    if os.path.exists("Data/predictions.csv"):
        os.remove("Data/predictions.csv")

    model = OscarWinnerModel(train_df, test_df)
    model.train_test()


def startup():
    demo, sample = Utils.mode_selector()

    if demo:
        Dataset().createDEMO(sample)
        return sample, Dataset(f"Data/DEMO_{sample}.xlsx")
    return None, Dataset()


def processTestSet(test_loc="Data/movies_test _anon.xlsx"):
    """
    Processes the test dataset "movies_test _anon_sample.xlsx" into the processed Test Set "movies_test.xlsx"

    :param test_loc: The location of the Test Dataset.
    """
    df = Dataset(test_loc)
    pc = ProcessColumns(df)

    new_df = pc.addBlankColumn('Oscar Winners', 0) \
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
        .dropColumn('Release Date (US)') \
        .dropColumn('Script Type') \
        .dropColumn('Primary Genre') \
        .dropColumn('Film')

    processed_df = new_df.dataset

    # Save the processed dataset to a new Excel file.
    processed_df.to_excel('Data/movies_test.xlsx', index=False)
    print("Processed Dataframe (movies_test) is now created!\n")


def processTrainSet(df):
    """
    Processes the original dataset "movies.xlsx" into the processed Train Set "movies_train.xlsx"

    :param df: Dataset object to be preprocessed.
    """
    # Initialize ProcessColumns object for further processing.
    pc = ProcessColumns(df)

    # Generate IMDb data if not already present.
    if not os.path.exists('Data/imdb_data.xlsx'):
        pc.generateIMDbData()

    # Perform various data processing steps.
    new_df = pc.addBlankColumn('ID', 0) \
        .processIMDbRating() \
        .processOscarWinner() \
        .processReleaseDate() \
        .processPrimaryGenre() \
        .processOneHotEncoder('Script Type', "SType") \
        .addBlankColumn('SType_based on a true story, remake', False) \
        .addBlankColumn('SType_semi-sequel', False) \
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
        .dropColumn('Release Date (US)') \
        .dropColumn('Script Type') \
        .dropColumn('Primary Genre') \
        .dropColumn('Film')

    processed_df = new_df.dataset

    # Save the processed dataset to a new Excel file.
    processed_df.to_excel('Data/movies_train.xlsx', index=False)
    print("Processed Dataframe (movies_test) is now created!\n")


if __name__ == '__main__':
    main()
