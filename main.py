import os
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    demo_num, df = startup()
    preprocessing(df)

    if os.path.exists(f"Data/Demos/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/Demos/DEMO_{demo_num}.xlsx")


def startup():
    yn = input("Do you want to use a demo of the dataset? (y / [n])\n")
    if yn:
        num = int(input("How many rows do you want in your demo?\n"))
        Dataset().createDEMO(num)
        return num, Dataset(f"Data/Demos/DEMO_{num}.xlsx")
    else:
        return None, Dataset()


def preprocessing(df):
    df.dropColumn('Distributor')
    df.dropColumn('Oscar Detail')
    df.dropColumn('Opening Weekend')
    df.dropColumn('Domestic Gross')
    df.dropColumn('Foreign Gross')
    df.dropColumn('Worldwide Gross')

    pc = ProcessColumns(df)

    # pc.processOscarWinner()
    # pc.processLabelEncoding('Script Type')
    # pc.processMinMaxScaler('Rotten Tomatoes  critics')
    # pc.processMinMaxScaler('Rotten Tomatoes Audience ')
    # pc.processMinMaxScaler('Metacritic  critics')
    # pc.processMinMaxScaler('Metacritic Audience ')
    # pc.processIMDbRating()
    # pc.processIMDBvsRTdisparity()

    df.showColumns("Film", "Release Date (US)")
    pc.processReleaseDate()
    df.showColumns("Film", "Release Date (US)")
    df.showColumnUnique('Release Date (US)')


if __name__ == '__main__':
    main()
