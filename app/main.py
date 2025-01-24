import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    while True:
        userInput = input()
        userTokens = userInput.split()
        if len(userTokens) != 0:
            match userTokens[0]:
                case "exit":
                    exitCode = int(userTokens[1])
                    sys.exit(exitCode)
                case "echo":
                    print(" ".join(userTokens[1:]))
                case _:
                    print(userInput + ": command not found")
        sys.stdout.write("$ ")


if __name__ == "__main__":
    main()
