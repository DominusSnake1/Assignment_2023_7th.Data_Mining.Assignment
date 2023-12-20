import os
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    # Initialize or load the dataset based on user input
    demo_num, df = startup()

    # Perform preprocessing steps on the dataset
    pp_df = preprocessing(df)

    # If a demo file was created, remove it
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")

    # Save the processed dataset to a new Excel file
    pp_df.to_excel('Data/processed_movies.xlsx', index=False)


def startup():
    """
    Function to determine whether to use a demo dataset or the complete dataset.

    :return: 1. Number of rows for the demo dataset.<br>
    2. Dataset object containing the loaded or created dataset.
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
    """
    # Drop columns not needed for processing.
    df.dropColumn('Distributor')
    df.dropColumn('Oscar Detail')
    df.dropColumn('Opening Weekend')
    df.dropColumn('Domestic Gross')
    df.dropColumn('Foreign Gross')
    df.dropColumn('Worldwide Gross')
    df.dropColumn('Genre')

    # Initialize ProcessColumns object for further processing.
    pc = ProcessColumns(df)

    # Generate IMDb data if not already present.
    if not os.path.exists('Data/imdb_data.xlsx'):
        pc.generateIMDbData()

    # Perform various data processing steps.
    pc.processIMDbRating()
    pc.processOscarWinner()
    pc.processReleaseDate()
    pc.processPrimaryGenre()

    # One-Hot encoding for categorical columns.
    pc.processOneHotEncoder('Script Type')
    pc.processOneHotEncoder('Primary Genre')

    # Min-Max scaling for numerical columns.
    pc.processMinMaxScaler('Rotten Tomatoes  critics')
    pc.processMinMaxScaler('Rotten Tomatoes Audience ')
    pc.processMinMaxScaler('Metacritic  critics')
    pc.processMinMaxScaler('Metacritic Audience ')
    pc.processMinMaxScaler('Average critics ')
    pc.processMinMaxScaler('Average audience ')
    pc.processMinMaxScaler('IMDb Rating')
    pc.processMinMaxScaler('Opening weekend ($million)')
    pc.processMinMaxScaler('Domestic gross ($million)')
    pc.processMinMaxScaler('Foreign Gross ($million)')
    pc.processMinMaxScaler('Worldwide Gross ($million)')
    pc.processMinMaxScaler('Budget ($million)')
    pc.processMinMaxScaler(' of Gross earned abroad', is_percentage=True)
    pc.processMinMaxScaler(' Budget recovered', is_percentage=True)
    pc.processMinMaxScaler(' Budget recovered opening weekend', is_percentage=True)

    # Deviance calculation for rating disparities.
    pc.processRatingDeviance('IMDB vs RT disparity',
                             'IMDb Rating',
                             'Rotten Tomatoes Audience ')
    pc.processRatingDeviance('Rotten Tomatoes vs Metacritic  deviance',
                             'Rotten Tomatoes  critics',
                             'Metacritic  critics')
    pc.processRatingDeviance('Audience vs Critics deviance ',
                             'Average audience ',
                             'Average critics ')

    return df


if __name__ == '__main__':
    main()
