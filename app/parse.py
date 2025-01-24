from enum import Enum
from enum import Enum
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
        return f"{self.token_type}: '{self.value}' whitespace: {self.followed_by_whitespace}"

    def __repr__(self):
        return f"{self.token_type}: '{self.value}' whitespace: {self.followed_by_whitespace}"

    def __getitem__(self, index):
        if index == 0:
            return self.token_type
        elif index == 1:
            return self.value
        elif index == 2:
            return self.followed_by_whitespace

    
def parse(userInput):
    userTokens = []
    quoteStack = []
    tokenString = ""
    for char in userInput:
        match char:
            case '"':
                if len(quoteStack) > 0 and quoteStack[-1] == '"':
                    quoteStack.pop()
                    userTokens.append(Token(tokenType.doubleQuote, tokenString,False))
                    tokenString = ""
                else:
                    tokenString += char
                    quoteStack.append('"')
            case "'":
                if len(quoteStack) > 0 and quoteStack[-1] == "'":
                    quoteStack.pop()
                    userTokens.append(Token(tokenType.singleQuote, tokenString,False))
                    tokenString = ""
                else:
                    quoteStack.append("'")
            case ' ':
                if len(quoteStack) == 0:
                    if len(tokenString) != 0:
                        userTokens.append(Token(tokenType.string, tokenString, False))
                    userTokens[-1].setFollowedByWhitespace(True)
                    tokenString = ""
                else:
                    tokenString += char
            case _:
                    tokenString += char
    if len(tokenString) != 0:
        userTokens.append(Token(tokenType.string, tokenString,False))
    return userTokens
