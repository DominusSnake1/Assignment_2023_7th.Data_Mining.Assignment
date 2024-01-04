import sys


def mode_selector():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == '-demo':
        if (args[1] == 'NUM_OF_ROWS') or (int(args[1]) <= 0):
            raise Exception('Please provide a positive number of rows.')
        return True, int(args[1])
    return False, -1
