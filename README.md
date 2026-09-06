The program takes as a command line argument the website URL we want to crawl by running
uv run main.py BASE_URL
where BASE_URL is the root URL of the website to crawl

Some random notes:

5. Next steps for Extending the Project (ideas from Bootdev)

- Make the script run on a timer and deploy it to a server. Have it email you every so often with the JSON report.

- Add more robust error checking so that you can crawl larger sites without issues.

- Count external links, as well as internal links, and add them to the report

- Use a graphics library to create an image that shows the links between the pages as a graph visualization

- Add a README.md file explaining to users how to clone your git repo and get started

4. asyncio is a completely new concept to me. For this portion of the code, I used the help of an LLM and heavily modified the existing code in crawl.py and main.py. Now the task
is really to full comprehend the code after the the project is finished and re-write the original version without asyncio so that I can compare the two versions at the same time.

3. When implementing the recursive crawling funciton logic, it is the first time I actually see recursion's use in a "production" environment. Also the mechanism that I
use hashset or hashmap (in this case) to check whether a site has already been "visited", in this case, crawled, is pretty cool. Much more lively than writing a DFS recursion on Leet Code.

2. Finally get to use Requests library, also cleanly written documentation

1. BeautifulSoup has a very readable documentation
