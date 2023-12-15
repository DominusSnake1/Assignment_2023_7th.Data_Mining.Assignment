import os.path
from Classes.Preprocessing import ProcessColumns
from Classes.Dataset import Dataset


def main():
    df = Dataset()
    df.createDEMO(5)
    df = Dataset("Data/Demos/DEMO_5.xlsx")
    pc = ProcessColumns(df)

    if not os.path.exists("Data/imdb_data.xlsx"):
        pc.getIMDbData()

    # pc.processOscarWinner()
    # pc.processLabelEncoding('Script Type')
    # pc.processMinMaxScaler('Rotten Tomatoes  critics')
    # pc.processMinMaxScaler('Rotten Tomatoes Audience ')
    # pc.processMinMaxScaler('Metacritic  critics')
    # pc.processMinMaxScaler('Metacritic Audience ')


if __name__ == '__main__':
    main()
