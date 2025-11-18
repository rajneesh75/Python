import argparse

parser = argparse.ArgumentParser(description='Sort some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')

parser.add_argument(dest='accumulate',
                    action='store_const',
                    const=sorted,
                    help='sort the integers')

args = parser.parse_args()
print(args.accumulate(args.integers))
