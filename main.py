import os
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    # Initialize or load the dataset based on user input
    demo_num, df = startup()

    # Perform preprocessing steps on the dataset
    processed_df = preprocessing(df)

    # Save the processed dataset to a new Excel file
    processed_df.to_excel('Data/processed_movies.xlsx', index=False)

    # If a demo file was created, remove it
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
        pc.generateIMDbData(df)

    # Perform various data processing steps.
    new_df = df
    new_df = pc.processIMDbRating(new_df)
    new_df = pc.processOscarWinner(new_df)
    new_df = pc.processReleaseDate(new_df)
    new_df = pc.processPrimaryGenre(new_df)

    # One-Hot encoding for categorical columns.
    new_df = pc.processOneHotEncoder(new_df, 'Script Type')
    new_df = pc.processOneHotEncoder(new_df, 'Primary Genre')

    # Min-Max scaling for numerical columns.
    new_df = pc.processMinMaxScaler(new_df, 'Rotten Tomatoes  critics')
    new_df = pc.processMinMaxScaler(new_df, 'Rotten Tomatoes Audience ')
    new_df = pc.processMinMaxScaler(new_df, 'Metacritic  critics')
    new_df = pc.processMinMaxScaler(new_df, 'Metacritic Audience ')
    new_df = pc.processMinMaxScaler(new_df, 'Average critics ')
    new_df = pc.processMinMaxScaler(new_df, 'Average audience ')
    new_df = pc.processMinMaxScaler(new_df, 'IMDb Rating')
    new_df = pc.processMinMaxScaler(new_df, 'Opening weekend ($million)')
    new_df = pc.processMinMaxScaler(new_df, 'Domestic gross ($million)')
    new_df = pc.processMinMaxScaler(new_df, 'Foreign Gross ($million)')
    new_df = pc.processMinMaxScaler(new_df, 'Worldwide Gross ($million)')
    new_df = pc.processMinMaxScaler(new_df, 'Budget ($million)')
    new_df = pc.processMinMaxScaler(new_df, ' of Gross earned abroad', is_percentage=True)
    new_df = pc.processMinMaxScaler(new_df, ' Budget recovered', is_percentage=True)
    new_df = pc.processMinMaxScaler(new_df, ' Budget recovered opening weekend', is_percentage=True)

    # Deviance calculation for rating disparities.
    new_df = pc.processRatingDeviance(new_df,
                                      'IMDB vs RT disparity',
                                      'IMDb Rating',
                                      'Rotten Tomatoes Audience ')
    new_df = pc.processRatingDeviance(new_df,
                                      'Rotten Tomatoes vs Metacritic  deviance',
                                      'Rotten Tomatoes  critics',
                                      'Metacritic  critics')
    new_df = pc.processRatingDeviance(new_df,
                                      'Audience vs Critics deviance ',
                                      'Average audience ',
                                      'Average critics ')

    return new_df


if __name__ == '__main__':
    main()
