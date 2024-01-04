import ast
import socket
import time
from sklearn import preprocessing
import pandas as pd
import imdb


class ProcessColumns:
    def __init__(self, dataset):
        self.dataset = dataset

    def processOneHotEncoder(self, column, _prefix):
        """
        Apply One-Hot Encoding to the specified column.

        :param _prefix: Adds a prefix into the column name.
        :param column: Column name to apply One-Hot Encoding.
        """
        df_encoded = pd.get_dummies(self.dataset[column], prefix=_prefix)

        self.dataset = pd.concat([self.dataset, df_encoded], axis=1)

        return self

    def processMinMaxScaler(self, column, is_percentage=False):
        """
        Apply Min-Max Scaling to the specified column.

        :param column: Column name to apply Min-Max Scaling.
        :param is_percentage: Flag indicating if the data is in percentage format (Defaults at `False`).
        """
        self.dataset[column] = self.dataset[column].replace('-', pd.NA)

        if is_percentage:
            self.dataset[column] = pd.to_numeric(self.dataset[column].str.rstrip('%'), errors='coerce')
        else:
            self.dataset[column] = pd.to_numeric(self.dataset[column], errors='coerce')

        self.dataset[column] = self.dataset[column].fillna(self.dataset[column].mean())
        self.dataset[column] = self.dataset[column].astype(int)

        min_max_scaler = preprocessing.MinMaxScaler()
        self.dataset[column] = min_max_scaler.fit_transform(self.dataset[[column]])
        self.dataset[column] = self.dataset[column].round(3)

        return self

    def processOscarWinner(self):
        """
         Map 'Oscar Winners' column to binary values based on the presence of 'Oscar winner' in the data.
         """
        def __OscarWinner_map_helper(x):
            if x in ["Oscar winner", "Oscar Winner"]:
                return 1
            return 0

        self.dataset['Oscar Winners'] = self.dataset['Oscar Winners'].map(__OscarWinner_map_helper)

        return self

    def generateIMDbData(self, batch_size=100, final_output_path='Data/imdb_data.xlsx'):
        """
        Retrieve IMDb data for movies in batches with missing IMDb ratings and save the data to a final Excel file.

        :param batch_size: The number of rows to process in each batch.
        :param final_output_path: The path for the final Excel file.
        """
        def __get_imdb_data(movie_title):
            api = imdb.Cinemagoer()
            movie_title = str(movie_title)
            retries = 0
            max_retries = 3

            while retries < max_retries:
                try:
                    movies = api.search_movie(movie_title)

                    if movies is None:
                        return None
                    movie = api.get_movie(movies[0].movieID)
                    return movie.data
                except (socket.timeout, imdb.IMDbDataAccessError):
                    time.sleep(5)
                    retries += 1

            print(f"Failed to retrieve IMDb data for '{movie_title}' after {max_retries} retries.")
            return None

        print("\nGetting the IMDb Data...")

        total_rows = self.dataset.shape[0]
        imdb_data_batches = []
        included_columns = ['localized title', 'rating', 'imdbID', 'genres']

        for start_index in range(0, total_rows, batch_size):
            end_index = min(start_index + batch_size, total_rows)
            batch_df = self.dataset.iloc[start_index:end_index]
            imdb_data_list = []

            for index, row in batch_df.iterrows():
                if not pd.isna(row['IMDb Rating']):
                    continue
                title = row['Film']
                imdb_data = __get_imdb_data(title)

                if imdb_data is None:
                    continue

                if 'rating' not in imdb_data.keys():
                    imdb_data['rating'] = 0
                if 'genres' not in imdb_data.keys():
                    imdb_data['genres'] = ['Not Available']

                new_row_dict = {key: imdb_data[key] for key in included_columns if key in imdb_data}
                imdb_data_list.append(new_row_dict)
                current_progress = round(((index / total_rows) * 100), 2)
                print(f"\r{current_progress} % Complete", end='', flush=True)

            imdb_data_batches.append(pd.DataFrame(imdb_data_list))

        print("\r100 % Complete!\n", flush=True)
        final_imdb_data = pd.concat(imdb_data_batches, ignore_index=True)
        final_imdb_data.rename(columns={"localized title": "Film"}, inplace=True)
        final_imdb_data.to_excel(final_output_path, index=False)
        print(f"Final IMDb Data is now saved in `{final_output_path}`.")

    def processIMDbRating(self):
        """
        Process IMDb ratings by filling missing values and scaling.
        """
        imdb_data = pd.read_excel('Data/imdb_data.xlsx')
        imdb_data['rating'] = imdb_data['rating'].fillna(imdb_data['rating'].mean())
        imdb_data['rating'] = imdb_data['rating'] * 10
        self.dataset['IMDb Rating'] = imdb_data['rating'].astype(int)

        return self

    def processRatingDeviance(self, target, column1, column2):
        """
        Calculate and create a new column for the deviance between two rating columns.

        :param target: New column name for storing the deviance.
        :param column1: First rating column.
        :param column2: Second rating column.
        """
        self.dataset[target] = self.dataset[column1] - self.dataset[column2]

        return self

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

        self.dataset['Release Date (US)'] = pd.to_datetime(self.dataset['Release Date (US)'], errors='coerce')
        self.dataset['Release Date (US)'] = self.dataset['Release Date (US)'].dt.month.map(__get_season)

        df_encoded = pd.get_dummies(self.dataset['Release Date (US)'], prefix='Season')

        self.dataset = pd.concat([self.dataset, df_encoded], axis=1)

        return self

    def processPrimaryGenre(self):
        imdb_data = pd.read_excel('Data/imdb_data.xlsx')
        self.dataset['Primary Genre'] = imdb_data['genres'].apply(lambda x: ast.literal_eval(x)[0] if pd.notna(x) else None)

        return self

    def dropColumn(self, column):
        """
        Drop a specified column from the DataFrame.

        :param column: Name of the column to drop.
        """
        self.dataset.drop(column, axis=1, inplace=True)
        print(f"'{column}' is dropped from the dataframe.")

        return self

    def addBlankColumn(self, columnName):
        self.dataset[columnName] = 0

        return self
