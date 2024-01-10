from enum import Enum


def isskippable(string):
    return string == " " or string == "\n" or string == "\t"


def shift(chars: list):
    char = chars.pop(0)
    if not isskippable(char):
        most_recent = char
    return char


class token_list:
    def __init__(self, list) -> None:
        self.list = list

    def __str__(self) -> str:
        string = "[ \n"
        for token in self.list:
            string += "\t" + token.__str__() + ", \n"

        string += "]"
        return string


class java_function:
    def __init__(self, target, code) -> None:
        self.target: str = target
        self.code: str = code


    def __str__(self) -> str:
        return f"{self.target}, {self.code}"


class token_type(Enum):
    UIMPL = "UIMPL" # unimplemented
#    INCL = "INCL" # incomplete
    EOF = "EOF" # end of file
    NUM = "NUM"
    BOOL = "BOOL"
    OPERATION = "OPERATION"
    COLON = "COLON"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    ITEM = "ITEM"
    MOD_ID = "MOD_ID"
    JAVA_FUNCTION = "JAVA_FUNCTION"
    LAMBDA = "LAMBDA"


class token:
    def __init__(self, value: str, t_type: token_type) -> None:
        self.value: str = value
        self.type: token_type = t_type

    def __str__(self) -> str:
        return f"token({self.value}, {self.type})"
    

records = {
    "true": token_type.BOOL,
    "false": token_type.BOOL,
    "item": token_type.ITEM,
    "mod_id": token_type.MOD_ID
}


def tokenize(content: str) -> list:

    tokens = []
    chars = [char for char in content]
    while len(chars) > 0:
        if chars[0] == "+" or chars[0] == "-" or chars[0] == "*" or chars[0] == "/": # Op
            tokens.append(token(shift(chars), token_type.OPERATION))
        elif chars[0] == "\"": # start of string
            string = ""
            shift(chars)
            while len(chars) > 0:
                if chars[0] != "\"": # not end of string
                    string+=shift(chars)
                else:
                    shift(chars)
                    break
            # insert check for missing end quote
            tokens.append(token(string, token_type.STRING))
        elif chars[0] == "(":
            code = None
            target = None
            lambdaFound = False
            shift(chars)
            while len(chars) > 0 and chars[0] != ")":
                if chars[0].isalpha() and target == None:
                    target = "";
                    while len(chars) > 0 and chars[0].isalpha():
                        target+=shift(chars)
                elif chars[0] == "-" and lambdaFound == False:
                    shift(chars)
                    if len(chars) > 0:
                        if chars[0] == ">":
                            shift(chars)
                            lambdaFound = True
                            tokens.append(token("->", token_type.LAMBDA))
                        else:
                            tokens.append(token(None, token_type.EOF))
                elif chars[0] == "{" and code == None:
                    code = ""
                    shift(chars)
                    while len(chars) > 0:
                        if chars[0] != "}":
                            code+=shift(chars)
                        else:
                            shift(chars)
                            break
                    if len(chars) == 0:
                        tokens.append(token(None, token_type.EOF))
                elif isskippable(chars[0]):
                    shift(chars)
                else:
                    tokens.append(token(shift(chars), token_type.UIMPL))
            if len(chars) > 0:
                if chars[0] == ")":
                    shift(chars)
                    tokens.append(token(java_function(target, code), token_type.JAVA_FUNCTION))
                else:
                    tokens.append(token(None, token_type.EOF))
            else:
                tokens.append(token(None, token_type.EOF))
            pass
        else:
            if chars[0].isdigit():
                num = ""
                while len(chars) > 0 and chars[0].isdigit():
                    num += shift(chars)
                tokens.append(token(num, token_type.NUM))

            elif chars[0].isalpha():
                ident = "";
                while len(chars) > 0 and chars[0].isalpha():
                    ident+=shift(chars)
                
                reserved = records.get(ident)
                if reserved == None:
                    tokens.append(token(ident, token_type.IDENTIFIER))
                else:
                    tokens.append(token(ident, reserved));
            elif isskippable(chars[0]):
                shift(chars)
            
            else:
                tokens.append(token(shift(chars), token_type.UIMPL))

    return token_list(tokens)