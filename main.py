import os
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    demo_num, df = startup()
    preprocessing(df)

    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")

    df.to_excel('Data/processed_movies.xlsx', index=False)


def startup():
    yn = input("Do you want to use a demo of the dataset? (y / [n])\n")

    if yn.lower() == "n":
        return None, Dataset()

    num = int(input("How many rows do you want in your demo?\n"))
    Dataset().createDEMO(num)
    return num, Dataset(f"Data/DEMO_{num}.xlsx")


def preprocessing(df):
    df.dropColumn('Distributor')
    df.dropColumn('Oscar Detail')
    df.dropColumn('Opening Weekend')
    df.dropColumn('Domestic Gross')
    df.dropColumn('Foreign Gross')
    df.dropColumn('Worldwide Gross')
    df.dropColumn('Genre')

    pc = ProcessColumns(df)

    if not os.path.exists('Data/imdb_data.xlsx'):
        pc.generateIMDbData()

    pc.processIMDbRating()
    pc.processOscarWinner()
    pc.processReleaseDate()
    pc.processPrimaryGenre()
    pc.processLabelEncoding('Script Type')
    pc.processLabelEncoding('Primary Genre')
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
    pc.processRatingDeviance('IMDB vs RT disparity',
                             'IMDb Rating',
                             'Rotten Tomatoes Audience ')
    pc.processRatingDeviance('Rotten Tomatoes vs Metacritic  deviance',
                             'Rotten Tomatoes  critics',
                             'Metacritic  critics')
    pc.processRatingDeviance('Audience vs Critics deviance ',
                             'Average audience ',
                             'Average critics ')


if __name__ == '__main__':
    main()
