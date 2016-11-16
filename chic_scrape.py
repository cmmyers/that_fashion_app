from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import time
import random

def get_post(query):
    url = "http://www.chictopia.com/photo/show/%s" % query
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')

    db_name = raw_input("Database name: ")
    collection = raw_input("Collection name: ")


    db = client[db_name]
    posts = db[collection]

    go_ahead = raw_input("Do you want to scrape? y/n ")

    if go_ahead == 'y':
        start = raw_input("Begin with id: ")
        end = raw_input("End with id: ")
        nums_list = xrange(int(start), int(end))

        ct = 0
        start = time.time()
        for i in nums_list:

            try:
                response = get_post(i)
                posts.insert({'id': int(i), 'html':str(response)})
            except ConnectionError:
                print "{} failed to respond".format(i)
            ct+=1
            if ct == 1:
                print "First record scraped!"
            if ct%100 == 0:
                end = time.time()
                print "Scraped {} records".format(ct)
                print "Elapsed time {} seconds".format(end-start)

    print "Done!"
