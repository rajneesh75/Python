import argparse

parser = argparse.ArgumentParser(description='average some integers.')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')

parser.add_argument(dest='sum',
                    action='store_const',
                    const=sum,
                    help='avg the integers')

parser.add_argument(dest='count',
                    action='store_const',
                    const=len)

args = parser.parse_args()
add = args.sum(args.integers)
count = args.count(args.integers)
average = add / count
print(average)
