import sys
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
        print(command[0] + ": not found")

commandDict = {
    "exit": cmdExit,
    "echo": cmdEcho,
    "type": cmdType,
}
