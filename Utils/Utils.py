import sys


def mode_selector():
    args = sys.argv[1:]

    if args[0] == '-demo':
        if (args[1] == 'NUM_OF_ROWS') or (int(args[1]) <= 0):
            raise Exception('Please provide a positive number of rows.')
        return True, int(args[1])
    return False, -1


def algorithm_selector():
    def exception():
        raise Exception('Please choose an algorithm from the list:\n'
                        '1. Logistic Regression [LR]\n'
                        '2. DecisionTreeClassifier [DTC]\n'
                        '3. RandomForestClassifier [RFC]\n'
                        '4. KNeighborsClassifier [KNN]\n')

    args = sys.argv[1:]

    algoriths = ['LR', 'DTC', 'RFC', 'KNN']

    if args[0] == '-demo' and args[2] == '-alg':
        if args[3] == 'SELECT_ALGORITHM' or args[3] not in algoriths:
            exception()
        return args[3]

    if args[0] == '-alg':
        if args[1] == 'SELECT_ALGORITHM' or (args[1] not in algoriths):
            exception()

        return args[1]
