import argparse

parser = argparse.ArgumentParser(description='some Description of your program')

parser.add_argument("input1", type=int, help="Enter an integer")
parser.add_argument("input2", type=float, help="Enter a float")
parser.add_argument("input3", default="John Doe", type=str, help="Enter a string")

args = parser.parse_args([input1, input2, input3])
print(args.input1)
print(args.input2)
print(args.input3)

