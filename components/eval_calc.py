import sys

if __name__ == "__main__":
    expression = " ".join(sys.argv[1:])
    print(eval(expression), end="")
