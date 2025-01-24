from posix import chdir
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
        fullPath = os.path.join(path, userTokens[0][1])
        if os.path.exists(fullPath):
            foundCommand = fullPath
    if foundCommand:
        return (parse.tokenType.string, foundCommand)
    else:
        print(f"{userTokens[0][1]}: not found")
        return None

def cmdExit(commandArgs):
    if len(commandArgs) != 0:
        exitCode = int(commandArgs[0][1])
    else:
        exitCode = 0
    sys.exit(exitCode)

    
def cmdEcho(commandArgs):
    output = ""
    for arg in commandArgs:
            output += arg[1]
    print(output.strip())

def cmdType(commandArgs):
    try:
        commandDict[commandArgs[0][1]]
        print(commandArgs[0][1] + " is a shell builtin")
    except KeyError:
        pathCommand = pathFallback(commandArgs)
        if pathCommand is not None:
            print(commandArgs[0][1] + " is "+ pathCommand)

def cmdExec(commandArgs):
    pathCommand = commandArgs[0][1].split(os.sep)[-1]
    try:
        commandDict[commandArgs[0][1]](commandArgs[1:])
    except KeyError:
        output = ""
        for arg in commandArgs[1:]:
            match arg[0]:
                case parse.tokenType.string | parse.tokenType.whitespace:
                    output += arg[1]
                case parse.tokenType.singleQuote:
                    output += "'" + arg[1] + "'"
                case parse.tokenType.doubleQuote:
                    output += '"' + arg[1] + '"'
        toSendToOs = pathCommand+ " " + output
        os.system(toSendToOs)

def cmdPwd(_):
    print(os.getcwd())

def cmdCd(commandArgs):
    if len(commandArgs) < 1:
        print("Usage: cd <directory>")
        return
    cdDir = os.path.expanduser(commandArgs[1][1])
    if not os.path.exists(cdDir):
        print(f"cd: {commandArgs[1][1]}: No such file or directory")
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
