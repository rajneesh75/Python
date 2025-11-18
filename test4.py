import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Your name")
parser.add_argument("--age", type=int, help="Your age (optional)")
parser.add_argument("--sex", type=str, help="Your sex (optional)")

user_input = input("Enter arguments (name [age] [sex]): ")
args = parser.parse_args(user_input.split())
print(f"Hello, {args.name}! You are {args.age} years old (if provided).You are a {args.sex} (if provided)")
