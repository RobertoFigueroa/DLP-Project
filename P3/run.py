import os
import sys


def run(input_file):
    os.system(f"python3 custom_scanner.py {input_file}")
    os.system("python3 custom_parser.py")
    

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("No file detected")
    else:
        run(sys.argv[1])
