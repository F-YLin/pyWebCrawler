The program takes as a command line argument the website URL we want to crawl by running
uv run main.py BASE_URL
where BASE_URL is the root URL of the website to crawl

Some random notes:
1. BeautifulSoup has a very readable documentation

2. Finally get to use Requests library, also cleanly written documentation

3. When implementing the recursive crawling funciton logic, it is the first time I actually see recursion's use in a "production" environment. Also the mechanism that I
use hashset or hashmap (in this case) to check whether a site has already been "visited", in this case, crawled, is pretty cool. Much more lively than writing a DFS recursion on Leet Code.