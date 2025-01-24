from enum import Enum
import sys
from enum import Enum
from typing import Tuple
class tokenType(Enum):
    string = 0
    singleQuote = 1
    doubleQuote = 2
type token = Tuple[tokenType, str]
def parse(userInput):
    userTokens = []
    quoteStack = []
    tokenString = ""
    for char in userInput:
        match char:
            case '"':
                if len(quoteStack) > 0 and quoteStack[-1] == '"':
                    quoteStack.pop()
                    userTokens.append((tokenType.doubleQuote, tokenString))
                    tokenString = ""
                else:
                    quoteStack.append('"')
            case "'":
                if len(quoteStack) > 0 and quoteStack[-1] == "'":
                    quoteStack.pop()
                    userTokens.append((tokenType.singleQuote, tokenString))
                    tokenString = ""
                else:
                    quoteStack.append("'")
            case ' ':
                if len(quoteStack) == 0:
                    userTokens.append((tokenType.string, tokenString))
                    tokenString = ""
                else:
                    tokenString += char
            case _:
                    tokenString += char
    if len(tokenString) != 0:
        userTokens.append((tokenType.string, tokenString))
    return userTokens
