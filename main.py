import os
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    # Initialize or load the dataset based on user input.
    demo_num, dataset = startup()

    # Perform preprocessing steps on the dataset.
    processed_df = preprocessing(dataset)

    # Save the processed dataset to a new Excel file.
    processed_df.to_excel('Data/processed_movies.xlsx', index=False)

    # If a demo file was created, remove it.
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")


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


def preprocessing(df):
    """
    Function to perform preprocessing steps on the dataset.

    :param df: Dataset object to be preprocessed.
    :return: The new processed dataframe.
    """
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

    return new_df.dataset


if __name__ == '__main__':
    main()
