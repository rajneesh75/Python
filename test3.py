import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('a', type=int)
    parser.add_argument('--b', type=int, required=False, default=10)
    a = input("enter a ")
    b = input("enter b ")
    args = parser.parse_args([a, b])
    print(args.a)
    print(args.b)


if __name__ == "__main__":
    main()
