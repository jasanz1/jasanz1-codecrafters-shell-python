import sys
import app.commands as commands
import app.parse as parse
import app.debug as debug
def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")
    commands.init()
    if len(sys.argv) > 1:
        debug.debugEnabled = True
    # Wait for user input
    while True:
        userInput = input()
        userInput = userInput.strip()
        userTokens = parse.parse(userInput)
        if len(userTokens) != 0:
            try:
                commands.commandDict[userTokens[0].value](userTokens[1:])
            except KeyError:
                fallBackCommand = commands.pathFallback(userTokens)
                if fallBackCommand is not None:
                    commands.cmdExec([fallBackCommand] + userTokens[1:])
                
        sys.stdout.write("$ ")


if __name__ == "__main__":
    main()
