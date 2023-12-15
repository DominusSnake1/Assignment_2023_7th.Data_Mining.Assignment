import pandas as pd


class Dataset(pd.DataFrame):
    def __init__(self, dataframe='Data/movies.xlsx'):
        super().__init__(pd.read_excel(dataframe))

    def createDEMO(self, X):
        DEMO = self.sample(X).copy()
        DEMO.to_excel(f'Data/Demos/DEMO_{X}.xlsx', index=False)

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

    def dropColumn(self, column):
        self.drop(column, axis=1, inplace=True)
        print(f"'{column}' is dropped from the dataframe.")

    def calculateMissingColumnDataPercentage(self):
        missing_data = self.isnull().sum()
        missing_percentage = (missing_data[missing_data > 0] / self.shape[0]) * 100
        missing_percentage.sort_values(ascending=True, inplace=True)

        return missing_percentage

    def calculateMissingIMDbRatings(self):
        missing_imdb_ratings = (100 - ((self['IMDb Rating'].count() / self.shape[0]) * 100)).round(2)
        print(f"{missing_imdb_ratings}% of the \"IMDb Rating\" values are missing from the dataset.")
