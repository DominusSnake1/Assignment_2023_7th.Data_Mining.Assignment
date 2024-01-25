from Classes.Dataset import Dataset
import sys
import os


def check_if_files_exist(dataset, demo_num):
    """
    Checks if some files exist and manages them accordingly.\n
    It removes the Demo Dataset and the predictions if they exist.
    If the train and test sets do not exist, they are created.

    :param dataset: The dataset to be processed.
    :param demo_num: The number of rows corresponding to the rows in the Demo Dataset.
    """
    # Process the Train Dataset.
    if not os.path.exists('Data/movies_train.xlsx'):
        from Classes.Preprocessing import processTrainSet
        processTrainSet(dataset)

    # If a demo file was created, remove it.
    if os.path.exists(f"Data/DEMO_{demo_num}.xlsx"):
        os.remove(f"Data/DEMO_{demo_num}.xlsx")

    # Process the Test Dataset.
    if not os.path.exists('Data/movies_test.xlsx'):
        from Classes.Preprocessing import processTestSet
        processTestSet()

    if os.path.exists("Data/predictions.csv"):
        os.remove("Data/predictions.csv")


def startup():
    """
    The function initiates the program by determining if the user wants to use a demo dataset.\n
    If the user wants a demo, it creates a demo dataset and returns the sample number and the corresponding Dataset instance.\n
    If not, it returns None and the default Dataset instance.

    :return: The sample number (int) and the Dataset instance.
    """
    if user_wants_demo():
        sample = demo_row_selector()
        Dataset().createDEMO(sample)
        return sample, Dataset(f"Data/DEMO_{sample}.xlsx")

    return None, Dataset()


def user_wants_demo():
    """
    The function checks if the user has requested to use a demo dataset according to the arguments.

    :return: TRUE if the user wants a demo, FALSE otherwise
    """
    args = sys.argv[1:]

    if len(args) <= 2:
        return False

    if args[2] != '-demo':
        raise Exception("In order to use a demo of the dataset, you must use '-demo' after selecting an algorithm.")

    return True


def demo_row_selector():
    """
        The function selects the number of rows for the demo dataset based on the given arguments, and returns it.

        :return: The number of rows for the demo dataset.
    """
    args = sys.argv[1:]

    if (len(args) < 4) or (args[3] == 'NUM_OF_ROWS') or (int(args[3]) <= 0):
        raise Exception('Please provide a positive number of rows.')

    return int(args[3])


def algorithm_selector():
    """
        The function selects the machine learning algorithm based on the given arguments,
        and it returns the selected algorith code.

        :return: The selected machine learning algorithm code.
    """
    args = sys.argv[1:]
    algorithms = ['LR', 'DTC', 'RFC', 'KNN']

    if (len(args) < 1) or (args[0] != '-alg'):
        raise Exception("In order to select an algorithm, you must use '-alg' after ./main.py.")

    if (len(args) < 2) or (args[1] == 'SELECT_ALGORITHM') or (args[1] not in algorithms):
        raise Exception('Please choose an algorithm from the list:\n'
                        '1. Logistic Regression [LR]\n'
                        '2. Decision Tree Classifier [DTC]\n'
                        '3. Random Forest Classifier [RFC]\n'
                        '4. KNeighbors Classifier [KNN]\n')

    return args[1]
