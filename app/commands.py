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

def cmdExit(code):
    if len(code) != 0:
        exitCode = int(code[0])
    else:
        exitCode = 0
    sys.exit(exitCode)

    
def cmdEcho(message):
    print(" ".join(message))

def cmdType(command):
    try:
        commandDict[command[0]]
        print(command[0] + " is a shell builtin")
    except KeyError:
        pathCommand = pathFallback(command)
        if pathCommand is not None:
            print(command[0] + " is "+ pathCommand)

def cmdExec(command):
    try:
        commandDict[command[0]](command[1:])
    except KeyError:
        os.system(" ".join(command))

commandDict = {
    "exit": cmdExit,
    "echo": cmdEcho,
    "type": cmdType,
    "exec": cmdExec
}
