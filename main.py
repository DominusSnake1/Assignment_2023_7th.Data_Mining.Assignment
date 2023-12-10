from sklearn import preprocessing
from Classes.Dataset import Dataset


def main():
    df = Dataset()
    # processScriptType(df)
    df.showColumns('Script Type', 'Primary Genre')

def processScriptType(df):
    df.showColumnUnique("Script Type")

    enc = preprocessing.LabelEncoder()
    df['Script Type'] = enc.fit_transform(df['Script Type'])

    df.showColumnUnique("Script Type")


if __name__ == '__main__':
    main()
