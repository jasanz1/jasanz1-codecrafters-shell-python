import sys
import app.commands as commands
def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    while True:
        userInput = input()
        userTokens = userInput.split()
        if len(userTokens) != 0:
            try:
                commands.commandDict[userTokens[0]](userTokens[1:])
            except KeyError:
                print(userInput + ": command not found")
        sys.stdout.write("$ ")


if __name__ == "__main__":
    main()
