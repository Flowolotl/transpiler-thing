import sys
import os
from tokens import token, token_list, token_type, records, tokenize
from util import settings


script_name = sys.argv[1]


def main():
    print(settings)
    split_name = script_name.split(".")
    if split_name[1] == "ffscript":
        if os.path.exists(script_name):
            readcontent = ""
            writecontent = ""
            with open(script_name, 'r') as file:
                readcontent = file.read()
            
            tokens = tokenize(readcontent)
            print(tokens)

            with open(split_name[0], 'w') as file:
                file.write(writecontent)


if __name__ == "__main__":
    main()