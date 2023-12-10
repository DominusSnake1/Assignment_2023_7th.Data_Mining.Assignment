import pandas as pd


class Dataset(pd.DataFrame):
    def __init__(self):
        super().__init__(pd.read_excel('Data/movies.xlsx'))

    def showDataframe(self):
        print(self)

    def showHead(self):
        print(self.head())

    def showAllColumnNames(self):
        print(self.columns.values.tolist())

    def showNumericalStats(self):
        print(self.describe().T)

    def showCategoricalStats(self):
        print(self.describe(include='object').T)

    def showColumnUnique(self, column):
        print(self[column].unique())

    def showColumns(self, *columns):
        print(self[list(columns)])

    def calculateMissingColumnDataPercentage(self):
        missing_data = self.isnull().sum()
        missing_percentage = (missing_data[missing_data > 0] / self.shape[0]) * 100
        missing_percentage.sort_values(ascending=True, inplace=True)

        return missing_percentage

    def calculateMissingIMDbRatings(self):
        missing_imdb_ratings = (100 - ((self['IMDb Rating'].count() / self.shape[0]) * 100)).round(2)
        print(f"{missing_imdb_ratings}% of the \"IMDb Rating\" values are missing from the dataset.")
