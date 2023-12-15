import os.path

from sklearn import preprocessing
import pandas as pd
import imdb


class ProcessColumns:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        # dataframe.dropColumn('Distributor')

    def processLabelEncoding(self, column):
        enc = preprocessing.LabelEncoder()
        self.dataframe[column] = enc.fit_transform(self.dataframe[column])

    def processMinMaxScaler(self, column):
        self.dataframe[column] = self.dataframe[column].replace('-', pd.NA)
        self.dataframe[column] = pd.to_numeric(self.dataframe[column], errors='coerce')
        self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].mean())
        self.dataframe[column] = self.dataframe[column].astype(int)

        min_max_scaler = preprocessing.MinMaxScaler()
        self.dataframe[column] = min_max_scaler.fit_transform(self.dataframe[[column]])

    def processOscarWinner(self):
        self.dataframe['Oscar Winners'] = self.dataframe['Oscar Winners'].map({'Oscar winner': 1, 'Oscar Winner': 1, 0: 0})

    def __generateIMDbData(self):
        def __get_imdb_data(movie_title):
            api = imdb.Cinemagoer()

            movie_title = str(movie_title)
            movies = api.search_movie(movie_title)

            if movies:
                movie = api.get_movie(movies[0].movieID)
                return movie.data
            else:
                return None

        print("Getting the IMDb Data...")

        total_rows = self.dataframe.shape[0]
        imdb_data_list = []

        included_columns = ['localized title', 'rating', 'imdbID']

        for index, row in self.dataframe.iterrows():
            if pd.isna(row['IMDb Rating']):
                title = row['Film']
                imdb_data = __get_imdb_data(title)

                if imdb_data is not None:
                    new_row_dict = {key: imdb_data[key] for key in included_columns if key in imdb_data}
                    imdb_data_list.append(new_row_dict)
                else:
                    print(f"\nFailed to retrieve IMDb data for '{title}'.\n")

            current_progress = round(((index / total_rows) * 100), 2)

            print(f"\r{current_progress}% Complete", end='', flush=True)

        print("\r100% Complete!\n", flush=True)

        new_dataframe = pd.DataFrame(imdb_data_list)
        new_dataframe.rename(columns={"localized title": "Film"}, inplace=True)
        if os.path.exists('Data/imdb_data.xlsx'):
            os.remove('Data/imdb_data.xlsx')
        new_dataframe.to_excel('Data/imdb_data.xlsx', index=False)

        print("IMDb Data is now saved in `Data/imdb_data.xlsx`.")

    def processIMDbRating(self):
        self.__generateIMDbData()

        imdb_data = pd.read_excel('Data/imdb_data.xlsx')
        self.dataframe['IMDb Rating'] = imdb_data['rating']
