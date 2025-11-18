import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')

parser.add_argument(dest='accumulate',
                    action='store_const',
                    const=sum,
                    help='sum the integers')

args = parser.parse_args()
print(args.accumulate(args.integers))
