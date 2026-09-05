import sys

from crawl import crawl_page, get_html

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

    #print(get_html(sys.argv[1]))

    page_data = crawl_page(sys.argv[1])

    print("Crawled pages:")
    print("----------")
    print(f"Number of crawled pages: {len(page_data)}")
    print("----------")

    # do something with the crawled data, e.g., save it to a file or database
    for page in page_data.values():
        print(page['heading'])

if __name__ == "__main__":
    main()
