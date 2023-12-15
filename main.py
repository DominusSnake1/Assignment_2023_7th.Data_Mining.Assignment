import os.path
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    df = Dataset()
    df.createDEMO(5)
    df = Dataset("Data/Demos/DEMO_5.xlsx")
    preprocessing(df)


def preprocessing(df):
    df.showAllColumnNames()
    df.dropColumn('Distributor')
    df.showAllColumnNames()
    pc = ProcessColumns(df)
    # pc.processOscarWinner()
    # pc.processLabelEncoding('Script Type')
    # pc.processMinMaxScaler('Rotten Tomatoes  critics')
    # pc.processMinMaxScaler('Rotten Tomatoes Audience ')
    # pc.processMinMaxScaler('Metacritic  critics')
    # pc.processMinMaxScaler('Metacritic Audience ')

    if not os.path.exists("Data/imdb_data.xlsx"):
        pc.getIMDbData()


if __name__ == '__main__':
    main()
