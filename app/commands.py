import sys
import os
import app.debug as debug
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
    foundPath = "" 
    for path in paths:
        fullPath = os.path.join(path, userTokens[0].value)
        if os.path.exists(fullPath):
            foundPath = path
            break
    if foundPath:
        return parse.Token(parse.tokenType.string, os.path.join(foundPath, userTokens[0].wrappedToken()),True)
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
    i =0 
    while i < len(commandArgs):
        if i < len(commandArgs)-1 and (commandArgs[i].token_type == parse.tokenType.redirect or commandArgs[i].token_type == parse.tokenType.append):
            break
        output += commandArgs[i].value
        if commandArgs[i].followed_by_whitespace: 
            output += " "
        elif i < len(commandArgs)-1 and commandArgs[i].token_type == parse.tokenType.string and commandArgs[i+1].token_type == parse.tokenType.string:
            output += " "
        i += 1
    if commandArgs[i].token_type == parse.tokenType.redirect:
        debug.debug(f"Redirecting {commandArgs[0].value} to {commandArgs[i+1].value}")
        with open(commandArgs[i+1].value, 'w', encoding='utf-8') as file:
            file.write(output)
        sys.stdout.write("/n")
        return
    elif commandArgs[i].token_type == parse.tokenType.append:
        debug.debug(f"Appending {commandArgs[0].value} to {commandArgs[i+1].value}")
        with open(commandArgs[i+1].value, 'a', encoding='utf-8') as file:
            file.write(output)
        sys.stdout.write("/n")
        return
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
        output = ""
        for arg in commandArgs[1:]:
            output += arg.wrappedToken()
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
