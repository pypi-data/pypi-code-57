import peper.recepies
import peper.bucket
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Compile a snippet.")
    parser.add_argument('recepie', type=str,
                        help='Recepie name')

    args = parser.parse_args()

    if args.recepie not in peper.recepies.l.keys():
        print("Recepie not found")
        exit()

    print("Instructions: ", peper.recepies.l[args.recepie]().instructions())
    print("Ingredients: ", peper.bucket.bucket)
