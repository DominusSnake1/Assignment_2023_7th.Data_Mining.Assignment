import pandas as pd


class Dataset(pd.DataFrame):
    def __init__(self, dataframe='Data/movies.xlsx'):
        """
        Constructor method to initialize the Dataset class.

        :param dataframe: Path to the Excel file containing movie data.
        If nothing is given as a path, it will default to the `movies.xlsx`.
        """
        super().__init__(pd.read_excel(dataframe))

    def createDEMO(self, X):
        """
        Create a sample dataset (DEMO) with a specified number of rows and save it to a new Excel file.

        :param X: Number of rows for the sample dataset.
        """
        DEMO = self.sample(X).copy()
        DEMO.to_excel(f'Data/DEMO_{X}.xlsx', index=False)

    def showDataframe(self):
        """
        Display the entire DataFrame.
        """
        print(self)

    def showHead(self):
        """
        Display the first few rows of the DataFrame.
        """
        print(self.head())

    def showAllColumnNames(self):
        """
        Display a list of all column names in the DataFrame.
        """
        print(self.columns.values.tolist())

    def showNumericalStats(self):
        """
        Display descriptive statistics for numerical columns in the DataFrame.
        """
        print(self.describe().T)

    def showCategoricalStats(self):
        """
        Display descriptive statistics for categorical columns in the DataFrame.
        """
        print(self.describe(include='object').T)

    def showColumnUnique(self, column):
        """
        Display unique values in a specified column of the DataFrame.

        :param column: Name of the column.
        """
        print(self[column].unique())

    def showColumns(self, *columns):
        """
        Display specified columns of the DataFrame.

        :param columns: Names of the columns to display.
        """
        print(self[list(columns)])

    def calculateMissingColumnDataPercentage(self):
        """
        Calculate the percentage of missing data for each column in the DataFrame.

        :return: The percentage of missing data for each column.
        """
        missing_data = self.isnull().sum()
        missing_percentage = (missing_data[missing_data > 0] / self.shape[0]) * 100
        missing_percentage.sort_values(ascending=True, inplace=True)

        return missing_percentage

    def calculateMissingIMDbRatings(self):
        """
        Calculate the percentage of missing IMDb Ratings in the DataFrame.
        """
        missing_imdb_ratings = (100 - ((self['IMDb Rating'].count() / self.shape[0]) * 100)).round(2)
        print(f"{missing_imdb_ratings}% of the \"IMDb Rating\" values are missing from the dataset.")
