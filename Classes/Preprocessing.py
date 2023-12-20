import ast
import os.path
import requests
from sklearn import preprocessing
import pandas as pd
import imdb
import json


class ProcessColumns:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def processOneHotEncoder(self, column):
        """
        Apply One-Hot Encoding to the specified column.

        :param column: Column name to apply One-Hot Encoding.
        """
        enc = preprocessing.LabelEncoder()
        self.dataframe[column] = enc.fit_transform(self.dataframe[column])

    def processMinMaxScaler(self, column, is_percentage=False):
        """
        Apply Min-Max Scaling to the specified column.

        :param column: Column name to apply Min-Max Scaling.
        :param is_percentage: Flag indicating if the data is in percentage format (Defaults at `False`).
        """
        self.dataframe[column] = self.dataframe[column].replace('-', pd.NA)

        if is_percentage:
            self.dataframe[column] = pd.to_numeric(self.dataframe[column].str.rstrip('%'), errors='coerce')
        else:
            self.dataframe[column] = pd.to_numeric(self.dataframe[column], errors='coerce')

        self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].mean())
        self.dataframe[column] = self.dataframe[column].astype(int)

        min_max_scaler = preprocessing.MinMaxScaler()
        self.dataframe[column] = min_max_scaler.fit_transform(self.dataframe[[column]])
        self.dataframe[column] = self.dataframe[column].round(3)

    def processOscarWinner(self):
        """
         Map 'Oscar Winners' column to binary values based on the presence of 'Oscar winner' in the data.
         """
        def __OscarWinner_map_helper(x):
            if x in ["Oscar winner", "Oscar Winner"]:
                return 1

            return 0

        self.dataframe['Oscar Winners'] = self.dataframe['Oscar Winners'].map(__OscarWinner_map_helper)

    def generateIMDbData(self):
        """
        Retrieve IMDb data for movies with missing IMDb ratings and save the data to 'Data/imdb_data.xlsx'.
        """
        def __get_imdb_data(movie_title):
            api = imdb.Cinemagoer()

            movie_title = str(movie_title)
            movies = api.search_movie(movie_title)

            if movies is None:
                return None

            movie = api.get_movie(movies[0].movieID)
            return movie.data

        print("\nGetting the IMDb Data...")

        total_rows = self.dataframe.shape[0]
        imdb_data_list = []

        included_columns = ['localized title', 'rating', 'imdbID', 'genres']

        for index, row in self.dataframe.iterrows():
            if not pd.isna(row['IMDb Rating']):
                continue

            title = row['Film']
            imdb_data = __get_imdb_data(title)

            if imdb_data is None:
                print(f"\nFailed to retrieve IMDb data for '{title}'.\n")
                continue

            if 'rating' not in imdb_data.keys():
                imdb_data['rating'] = 0

            if 'genres' not in imdb_data.keys():
                imdb_data['genres'] = "Not Available"

            new_row_dict = {key: imdb_data[key] for key in included_columns if key in imdb_data}
            imdb_data_list.append(new_row_dict)

            current_progress = round(((index / total_rows) * 100), 2)

            print(f"\r{current_progress} % Complete", end='', flush=True)

        print("\r100 % Complete!\n", flush=True)

        new_dataframe = pd.DataFrame(imdb_data_list)
        new_dataframe.rename(columns={"localized title": "Film"}, inplace=True)
        new_dataframe.to_excel('Data/imdb_data.xlsx', index=False)

        print("IMDb Data is now saved in `Data/imdb_data.xlsx`.")

    def processIMDbRating(self):
        """
        Process IMDb ratings by filling missing values and scaling.
        """
        imdb_data = pd.read_excel('Data/imdb_data.xlsx')
        imdb_data['rating'] = imdb_data['rating'].fillna(imdb_data['rating'].mean())
        imdb_data['rating'] = imdb_data['rating'] * 10
        self.dataframe['IMDb Rating'] = imdb_data['rating'].astype(int)

    def processRatingDeviance(self, target, column1, column2):
        """
        Calculate and create a new column for the deviance between two rating columns.

        :param target: New column name for storing the deviance.
        :param column1: First rating column.
        :param column2: Second rating column.
        """
        self.dataframe[target] = self.dataframe[column1] - self.dataframe[column2]

    def processReleaseDate(self):
        """
        Process the 'Release Date (US)' column by converting it to seasons and applying One-Hot Encoding.
        """
        def __get_season(month):
            if 3 <= month <= 5:
                return 'Spring'
            elif 6 <= month <= 8:
                return 'Summer'
            elif 9 <= month <= 11:
                return 'Autumn'
            else:
                return 'Winter'

        self.dataframe['Release Date (US)'] = pd.to_datetime(self.dataframe['Release Date (US)'], errors='coerce')
        self.dataframe['Release Date (US)'] = self.dataframe['Release Date (US)'].dt.month.map(__get_season)

        df_encoded = pd.get_dummies(self.dataframe['Release Date (US)'], prefix='Season')

        self.dataframe = pd.concat([self.dataframe, df_encoded], axis=1)

    def processPrimaryGenre(self):
        imdb_data = pd.read_excel('Data/imdb_data.xlsx')
        self.dataframe['Primary Genre'] = imdb_data['genres'].apply(lambda x: ast.literal_eval(x)[0] if pd.notna(x) else None)
