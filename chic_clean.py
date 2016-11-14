

import json
from bs4 import BeautifulSoup


def check_status(html):
    '''some entries either refer to urls with no photo or return an error
    this function will alert to pages that do not exist and flag pages that should
    rechecked'''
    soup = BeautifulSoup(html, "html.parser")
    output = ''
    text = str(soup.find())
    if text.startswith('<response [200]') or text.startswith('<response [404]'):
        output = 'check'
    elif soup.title.text == u"The page you are looking for doesn't exist | Chictopia":
        output = "DNE"
    else:
        output = "passed"

    return output

def extract_feats(html):
    soup = BeautifulSoup(html, "html.parser")
    #features dictionary
    fd = {}

    #find title of post
    title = soup.find("h1", { "class":"photo_title"})
    fd['title'] = title.text

    #find date of post
    #how to extract date? has to do with finding sibs or children
    #fd['date'] = title.findNextSibling.find().text

    #find smaller photos url
    subs = soup.find("div", {"class":"subphoto_items"})
    sub_photos = subs.findChildren("img")
    fd['subphotos'] = sub_photos

    #find main photo
    main_photo = soup.find("div", {"id" : "image_wrap"}).findChildren("img")
    fd['main_photo'] = main_photo

    #number of votes for this post
    votes = soup.find("div", {"id": "vote_text_100000", "class": "left action_unclicked_show cursor"}).text
    fd['votes'] = votes

    #number of comments for this post
    comments = soup.find("div", {"id": "comment_text_100000", "class": "left action_unclicked_show cursor"}).text
    fd['comments'] = comments

    #number of favorites for this post
    faves = soup.find("div", {"id": "favorite_text_100000", "class": "left action_unclicked_show cursor"}).text
    fd['favorites'] = faves

    #find all tags
    tags = soup.find("div", {"id": "tag_boxes"})
    fd['tags'] = tags

    #find description
    desc = soup.find("div", {"id", "photo_description"})
    fd['photo_desc'] = desc

    #

    ''''''
    return fd

def view_entry():
    with open(path) as json_data:
        for line in json_data:
            print json.loads(line)['html']


if __name__ == '__main__':
    # path = raw_input("Please enter the path to the json file you would like to clean ")
    path = 'chic_export_1.json'
    is_exists = []
    check = []
    features_collect = []
    with open(path) as json_data:
        for line in json_data:
            entry = json.loads(line)
            status = check_status(entry['html'])
            if status == 'passed':
                features = extract_feats(entry['html'])
                features_collect.append(features)
                is_exists.append(entry['id'])
            elif status == 'check':
                check.append(entry['id'])
        json_data.close()
