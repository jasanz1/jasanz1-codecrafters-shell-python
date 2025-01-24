import sys
def cmdExit(code,_):
    exitCode = int(code[0])
    sys.exit(exitCode)

    
def cmdEcho(message,_):
    print(message)

def cmdType(command,commandDict):
    try:
        print(commandDict[command[0]] + " is a shell builtin")
    except KeyError:
        print(command[0] + ": not found")

def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")
    commandDict = {
        "exit": cmdExit,
        "echo": cmdEcho,
    }

    # Wait for user input
    while True:
        userInput = input()
        userTokens = userInput.split()
        if len(userTokens) != 0:
            try:
                commandDict[userTokens[0]](userTokens[1:],commandDict)
            except KeyError:
                print(userInput + ": command not found")
        sys.stdout.write("$ ")


if __name__ == "__main__":
    main()
