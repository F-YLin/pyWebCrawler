
# aims to export to JASON so the extracted data from every page is easy to read and share
# plan to create a report.json file containing a list of all page records

import json 

def write_json_report(page_data, file_name="report.json"):
    # page_data is the dictionary returned by the crawler
    # keys are the normalized URLs and vals are the page data dictionaries
    # filename is the JSON file to create, which defaults to "report.json"

    # convert page_data_values() to a sorted list(sort by "url")
    pages = sorted(page_data.values(), key=lambda p: p['url'])

    # write the list to a JSON file using json.dump with indent=2
    with open(file_name, 'w', encoding="utf-8") as f:
        json.dump(pages, f, indent=2)

    



