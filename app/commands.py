import sys
import os
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
        fullPath = os.path.join(path, userTokens[0])
        if os.path.exists(fullPath):
            foundCommand = fullPath
    if foundCommand:
        return foundCommand
    else:
        print(f"{userTokens[0]}: not found")
        return None

def cmdExit(commandArgs):
    if len(commandArgs) != 0:
        exitCode = int(commandArgs[0])
    else:
        exitCode = 0
    sys.exit(exitCode)

    
def cmdEcho(commandArgs):
    print(" ".join(commandArgs))

def cmdType(commandArgs):
    try:
        commandDict[commandArgs[0]]
        print(commandArgs[0] + " is a shell builtin")
    except KeyError:
        pathCommand = pathFallback(commandArgs)
        if pathCommand is not None:
            print(commandArgs[0] + " is "+ pathCommand)

def cmdExec(commandArgs):
    pathCommand = commandArgs[0].split(os.sep)[-1]
    try:
        commandDict[commandArgs[0]](commandArgs[1:])
    except KeyError:
        os.system(" ".join([pathCommand] + commandArgs[1:]))

def cmdPwd(_):
    print(os.getcwd())

commandDict = {
    "exit": cmdExit,
    "echo": cmdEcho,
    "type": cmdType,
    "exec": cmdExec,
    "pwd" : cmdPwd,
}
