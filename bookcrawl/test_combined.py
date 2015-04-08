#!/usr/bin/python2
import page_lookup
import searcher
import os
import json

def lookup_na(name, author):
    url=""
    title=""
    pages=""
    execstring = "./searcher.py"
    print execstring
    os.system(execstring) 
    with open('search_result.json') as jsonfile:
        data = json.load(jsonfile)[0]
        title = data["s_title"]
        url = data["s_url"]
    page_lookup.lookup_pages_by_urls([url])
    with open('page_result.json') as jsonfile:
        pages=json.load(jsonfile)["p_pages"]
    print(title + " is " + pages + " pages long.")
    reactor.stop()
        

def main():
    lookup_na("computer networks","andrew tanenbaum")

if __name__ == "__main__":
    main()
