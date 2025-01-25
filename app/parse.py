from enum import Enum
import app.debug as debug
class tokenType(Enum):
    unknown = 0
    string = 1
    singleQuote = 2
    doubleQuote = 3
    whitespace = 4


class Token:
    def __init__(self, token_type, value, followed_by_whitespace):
        self.token_type = token_type
        self.value = value
        self.followed_by_whitespace = followed_by_whitespace

    def setFollowedByWhitespace(self, followed_by_whitespace):
        self.followed_by_whitespace = followed_by_whitespace
    def __str__(self):
        return f"<{self.token_type}: '{self.value}' whitespace: {self.followed_by_whitespace}>"

    def __repr__(self):
        return f"<{self.token_type}: '{self.value}' whitespace: {self.followed_by_whitespace}>"

    def __getitem__(self, index):
        if index == 0:
            return self.token_type
        elif index == 1:
            return self.value
        elif index == 2:
            return self.followed_by_whitespace

    
def parse(userInput):
    userTokens = []
    tokenString = ""
    i = 0
    while i < len(userInput):
        char = userInput[i]
        match char:
            case '"':
                doubleQuoteReturn,i = doubleQuote(userInput,i)
                userTokens.append(doubleQuoteReturn)
            case "'":
                singleQuoteReturn,i = singleQuote(userInput,i)
                userTokens.append(singleQuoteReturn)
            case '\\':
                escapedCharReturn,i = escapedChar(userInput,i)
                tokenString += escapedCharReturn
            case ' ':
                if len(userTokens) != 0:
                    userTokens[-1].setFollowedByWhitespace(True)
                    if len(tokenString) != 0:
                        userTokens.append(Token(tokenType.string, tokenString,False))
                else:
                    userTokens.append(Token(tokenType.whitespace, tokenString,True))
                tokenString = ""
            case _:
                tokenString += char
        i += 1
    if len(tokenString) != 0:
        userTokens.append(Token(tokenType.string, tokenString,False))
    debug.debug(f"userTokens: {userTokens}")
    return userTokens


def singleQuote(userInput,i):
    tokenString = ""
    i += 1
    while i < len(userInput):
        char = userInput[i]
        if char == "'":
            return (Token(tokenType.singleQuote, tokenString, False),i)
        else:
            tokenString += char
            i += 1
    return (Token(tokenType.singleQuote, tokenString, False),i)

def escapedChar(userInput,i):
    return (userInput[i+1],i+1)

def doubleQuote(userInput,i):
    tokenString = ""
    i += 1
    while i < len(userInput):
        char = userInput[i]
        debug.debug(f"tokenString: {userInput[i:]}")
        match char:
            case '"':
                return (Token(tokenType.doubleQuote, tokenString, False),i)
            case "'":
                singleQuoteReturn,i = singleQuote(userInput,i)
                tokenString += "'" + singleQuoteReturn.value + "'"
            case '\\':
                escapedCharReturn,i = escapedChar(userInput,i)
                tokenString += escapedCharReturn
            case _:
                tokenString += char
        i += 1
    return (Token(tokenType.doubleQuote, tokenString, False),i)
