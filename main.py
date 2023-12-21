import os
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    # Initialize or load the dataset based on user input.
    demo_num, df = startup()

    # Perform preprocessing steps on the dataset.
    processed_df = preprocessing(df)

    # Save the processed dataset to a new Excel file.
    processed_df.to_excel('Data/processed_movies.xlsx', index=False)

    # If a demo file was created, remove it.
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")


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
    # Initialize ProcessColumns object for further processing.
    pc = ProcessColumns(df)

    # Generate IMDb data if not already present.
    if not os.path.exists('Data/imdb_data.xlsx'):
        pc.generateIMDbData(df)

    # Perform various data processing steps.
    df = pc.processIMDbRating(df)
    df = pc.processOscarWinner(df)
    df = pc.processReleaseDate(df)
    df = pc.processPrimaryGenre(df)
    df = pc.processOneHotEncoder(df, 'Script Type')
    df = pc.processOneHotEncoder(df, 'Primary Genre')

    # Min-Max scaling for numerical columns.
    df = pc.processMinMaxScaler(df, 'Rotten Tomatoes  critics')
    df = pc.processMinMaxScaler(df, 'Rotten Tomatoes Audience ')
    df = pc.processMinMaxScaler(df, 'Metacritic  critics')
    df = pc.processMinMaxScaler(df, 'Metacritic Audience ')
    df = pc.processMinMaxScaler(df, 'Average critics ')
    df = pc.processMinMaxScaler(df, 'Average audience ')
    df = pc.processMinMaxScaler(df, 'IMDb Rating')
    df = pc.processMinMaxScaler(df, 'Opening weekend ($million)')
    df = pc.processMinMaxScaler(df, 'Domestic gross ($million)')
    df = pc.processMinMaxScaler(df, 'Foreign Gross ($million)')
    df = pc.processMinMaxScaler(df, 'Worldwide Gross ($million)')
    df = pc.processMinMaxScaler(df, 'Budget ($million)')
    df = pc.processMinMaxScaler(df, ' of Gross earned abroad', is_percentage=True)
    df = pc.processMinMaxScaler(df, ' Budget recovered', is_percentage=True)
    df = pc.processMinMaxScaler(df, ' Budget recovered opening weekend', is_percentage=True)

    # Deviance calculation for rating disparities.
    df = pc.processRatingDeviance(df,
                                  'IMDB vs RT disparity',
                                  'IMDb Rating',
                                  'Rotten Tomatoes Audience ')
    df = pc.processRatingDeviance(df,
                                  'Rotten Tomatoes vs Metacritic  deviance',
                                  'Rotten Tomatoes  critics',
                                  'Metacritic  critics')
    df = pc.processRatingDeviance(df,
                                  'Audience vs Critics deviance ',
                                  'Average audience ',
                                  'Average critics ')

    # Drop columns not needed for processing.
    df.dropColumn('Distributor')
    df.dropColumn('Oscar Detail')
    df.dropColumn('Opening Weekend')
    df.dropColumn('Domestic Gross')
    df.dropColumn('Foreign Gross')
    df.dropColumn('Worldwide Gross')
    df.dropColumn('Genre')
    df.dropColumn('Release Date (US)')

    return df


if __name__ == '__main__':
    main()
