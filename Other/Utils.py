from Classes.Dataset import Dataset
import sys


def startup():
    """
        The function initiates the program by determining if the user wants to use a demo dataset.\n
        If the user wants a demo, it creates a demo dataset and returns the sample number and the corresponding Dataset instance.\n
        If not, it returns None and an empty Dataset instance.

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
    algoriths = ['LR', 'DTC', 'RFC', 'KNN']

    if (len(args) < 1) or (args[0] != '-alg'):
        raise Exception("In order to select an algorithm, you must use '-alg' after ./main.py.")

    if (len(args) < 2) or (args[1] == 'SELECT_ALGORITHM') or (args[1] not in algoriths):
        raise Exception('Please choose an algorithm from the list:\n'
                        '1. Logistic Regression [LR]\n'
                        '2. DecisionTreeClassifier [DTC]\n'
                        '3. RandomForestClassifier [RFC]\n'
                        '4. KNeighborsClassifier [KNN]\n')

    return args[1]
