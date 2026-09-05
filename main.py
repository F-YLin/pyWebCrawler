import sys

def main():
    # # uv run example.py -v
    # print("Script name:", sys.argv[0])  # example.py
    # print("Argument:", sys.argv[1])     # -v

    # if the number of CLI arguments is less than 2
    # print error message and exit with code 1
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    # if the number of CLI arguments is more than 2
    # print error message and exit with code 1
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
        
    else:
        print(f"starting crawl of: {sys.argv[1]}")

if __name__ == "__main__":
    main()
