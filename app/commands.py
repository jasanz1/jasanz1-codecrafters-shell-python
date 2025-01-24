import sys
import os
import app.parse as parse
def init():
    global paths
    path_temp = os.environ.get("PATH")
    if path_temp is None:
        paths =  [] 
    else:
        paths = path_temp.split(os.pathsep)
    return paths

def pathFallback(userTokens):
    foundCommand = "" 
    for path in paths:
        fullPath = os.path.join(path, userTokens[0].value)
        if os.path.exists(fullPath):
            foundCommand = fullPath
    if foundCommand:
        return parse.Token(parse.tokenType.string, foundCommand,True)
    else:
        print(f"{userTokens[0].value}: not found")
        return None

def cmdExit(commandArgs):
    if len(commandArgs) != 0:
        exitCode = int(commandArgs[0].value)
    else:
        exitCode = 0
    sys.exit(exitCode)

    
def cmdEcho(commandArgs):
    output = ""
    for arg in commandArgs:
            if arg.followed_by_whitespace:
                output += arg.value + " "
            else:
                output += arg.value
    print(output.strip())

def cmdType(commandArgs):
    try:
        commandDict[commandArgs[0].value]
        print(commandArgs[0].value + " is a shell builtin")
    except KeyError:
        pathCommand = pathFallback(commandArgs)
        if pathCommand is not None:
            print(commandArgs[0].value + " is " + pathCommand[1])

def cmdExec(commandArgs):
    pathCommand = commandArgs[0].value.split(os.sep)[-1]
    try:
        commandDict[commandArgs[0].value](commandArgs[1:])
    except KeyError:
        print(str(commandArgs))
        output = ""
        for arg in commandArgs[1:]:
            match arg.token_type:
                case parse.tokenType.string:
                    output += arg.value
                case parse.tokenType.singleQuote:
                    output += "'" + arg.value + "'"
                case parse.tokenType.doubleQuote:
                    output += '"' + arg.value + '"'
            if arg.followed_by_whitespace:
                output += " "
        toSendToOs = pathCommand+ " " + output
        os.system(toSendToOs)

def cmdPwd(_):
    print(os.getcwd())

def cmdCd(commandArgs):
    if len(commandArgs) < 1:
        print("Usage: cd <directory>")
        return
    cdDir = os.path.expanduser(commandArgs[0].value)
    if not os.path.exists(cdDir):
        print(f"cd: {commandArgs[0].value}: No such file or directory")
        return
    os.chdir(cdDir)

commandDict = {
    "exit": cmdExit,
    "echo": cmdEcho,
    "type": cmdType,
    "exec": cmdExec,
    "pwd" : cmdPwd,
    "cd"  : cmdCd
}
