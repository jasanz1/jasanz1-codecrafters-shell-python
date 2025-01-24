import sys
import app.commands as commands
import os
def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")
    commands.init()

    # Wait for user input
    while True:
        userInput = input()
        userTokens = userInput.split()
        if len(userTokens) != 0:
            try:
                commands.commandDict[userTokens[0]](userTokens[1:])
            except KeyError:
                fallBackCommand = commands.pathFallback(userTokens)
                if fallBackCommand is not None:
                    commands.cmdExec([fallBackCommand] + userTokens[1:])
                
        sys.stdout.write("$ ")


if __name__ == "__main__":
    main()
