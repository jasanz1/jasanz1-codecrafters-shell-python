from enum import Enum
import app.debug as debug
class tokenType(Enum):
    unknown = 0
    string = 1
    singleQuote = 2
    doubleQuote = 3
    redirect = 4
    append = 5


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

    def wrappedToken(self):
        if self.token_type == tokenType.singleQuote:
            return f"'{self.value}'"
        elif self.token_type == tokenType.doubleQuote:
            return f'"{self.value}"'
        return f"{self.value}"


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
                    userTokens.append(Token(tokenType.string, tokenString,True))
                tokenString = ""
            case "1" | "2"  ">":
                redirectOrAppendReturn,i,tokenStringtemp = redirectOrAppend(userInput,i)
                if len(tokenString) != 0:
                    tokenString = tokenStringtemp
                else:
                    userTokens.append(redirectOrAppendReturn)
            case _:
                debug.debug(f"string     : {char}")
                tokenString += char
        i += 1
    if len(tokenString) != 0:
        userTokens.append(Token(tokenType.string, tokenString,False))
    debug.debug(f"userTokens: {userTokens}")
    return userTokens

def redirectOrAppend(userInput,i):
    tokenString = userInput[i] 
    debug.debug(f"roa        : {userInput[i:]}")
    i += 1
    debug.debug(f"roa        : {userInput[i:]}")
    if userInput[i] = " " or userInput[i] = ">":
        if userInput[i] = ">":
            tokenString += userInput[i] 
            i += 1
            debug.debug(f"roa        : {userInput[i:]}")
            return (Token(tokenType.append, tokenString,False),i,"")
        return (Token(tokenType.redirect, tokenString,False),i,"")
    if userInput[i] == ">":
        tokenString += userInput[i] 
        if userInput[i+1] == ">":
            i += 1
            debug.debug(f"roa        : {userInput[i:]}")
            tokenString += userInput[i] 
            return (Token(tokenType.append, tokenString,False),i,"") 
        else:
            return (Token(tokenType.redirect, tokenString,False),i,"") 
    return (Token(tokenType.string, tokenString,False),i,tokenString)

def singleQuote(userInput,i):
    tokenString = ""
    i += 1
    while i < len(userInput):
        char = userInput[i]
        debug.debug(f"singleQuote: {userInput[i:]}")
        if char == "'":
            return (Token(tokenType.singleQuote, tokenString, False),i)
        else:
            tokenString += char
            i += 1
    return (Token(tokenType.singleQuote, tokenString, False),i)

def escapedChar(userInput,i):
    debug.debug(f"escaped: {userInput[i+1:]}")
    return (userInput[i+1],i+1)

def doubleQuote(userInput,i):
    tokenString = ""
    i += 1
    while i < len(userInput):
        char = userInput[i]
        debug.debug(f"doubleQuote: {userInput[i:]}")
        match char:
            case '"':
                return (Token(tokenType.doubleQuote, tokenString, False),i)
            case '\\':
                if userInput[i+1] == "\\" or userInput[i+1] == '"' or userInput[i+1] == "$":
                    escapedCharReturn,i = escapedChar(userInput,i)
                    tokenString += escapedCharReturn
                else:
                    tokenString += char
            case _:
                tokenString += char
        i += 1
    return (Token(tokenType.doubleQuote, tokenString, False),i)
