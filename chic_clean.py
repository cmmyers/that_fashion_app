
from pymongo import MongoClient
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
    if title is not None:
        title = title.text
    else:
        fd['title'] = 'No Title'
    #find date of post
    date = soup.find("meta", {"itemprop":"dateCreated"})
    if date is not None:
        date = date.get("content")
        fd['date'] = str(date)
    else:
        fd['date'] = "No Date"

    #find smaller photos url
    sub_photos = soup.find("div", {"class":"subphoto_items"})
    if sub_photos is not None:
        sub_photos = sub_photos.findChildren("img")
        sub_photos = [photo.get("src") for photo in sub_photos]
        fd['subphotos'] = str(sub_photos)
    else:
        fd['subphotos'] = "No Subphotos"

    #find main photo
    main_photo = soup.find("div", {"id" : "image_wrap"})
    if main_photo is not None:
        main_photo = main_photo.findChild("img").get("src")
        fd['main_photo'] = str(main_photo)
    else:
        fd['main_photo'] = "No Main Photo"

    #number of votes for this post
    votes = soup.find("div", {"id": "vote_text_100000"})
    if votes is not None:
        votes = votes.text
        votes = int(votes.split()[0])
        fd['votes'] = int(votes)
    else:
        fd['votes'] = 0

    #number of comments for this post
    comments = soup.find("div", {"id": "comment_text_100000"})
    if comments is not None:
        comments = comments.text
        comments = int(comments.split()[0])
        fd['comments'] = int(comments)
    else:
        fd['comments'] = 0

    #number of favorites for this post
    faves = soup.find("div", {"id": "favorite_text_100000"})
    if faves is not None:
        faves = faves.text
        faves = int(faves.split()[0])
        fd['favorites'] = int(faves)
    else:
        fd['faves'] = 0

    #find all tags
    tags = soup.find("div", {"id": "tag_boxes"})
    if tags is not None:
        tags = tags.findChildren("a")
        tags = [tag.text for tag in tags]
        fd['tags'] = str(tags)
    else:
        fd['tags'] = "No Tags"

    #find description
    desc = soup.find("div", {"id": "photo_description"}).text
    fd['photo_desc'] = desc.encode('ascii', 'ignore')

    #find links to garments
    links = soup.find("div",{"class": "garmentLinks"})
    fd['garment_links'] = str(links)

    #find styleCouncl status
    style_council = soup.find("div", {"class":"help"}).findChild("img").get("alt")
    fd['style_council'] = str(style_council)

    #find number of followers
    followers = soup.find("div", {"id":"follow"}).text
    if followers != '\n\n':
        fd['followers'] = int(followers)
    else:
        fd['followers'] = 0

    #find username
    username = soup.find("div",{ "id":"name_div"}).findChild("a").text
    fd['username'] = str(username)


    #find location
    location = soup.find("div", {"id":"loc_div"}).findChild("a")
    if location is not  None:
        location = location.text
        fd['location'] = str(location)
    else:
        fd['location'] = "n/a"

    #find num chic points
    chic_points = soup.find("div", {"itemprop": "author"}).findChildren("div", {"class":"px10"})[2].text
    chic_points = chic_points.split()[0]
    fd['chic_points'] = int(chic_points)

    ''''''
    return fd

def view_entry():
    with open(path) as json_data:
        for line in json_data:
            print json.loads(line)['html']


if __name__ == '__main__':


    #path = raw_input("Please enter the path to the json file you would like to clean ")
    path = '../chic_data/chic_0-5000.json'
    is_exists = []
    check = []
    features_collect = []

    client = MongoClient('mongodb://localhost:27017/')

    db_name = raw_input("Database name: ")
    collection = raw_input("Collection name: ")

    db = client[db_name]
    posts = db[collection]

    ct = 1
    passed_ct = 0
    with open(path) as json_data:
        for line in json_data:
            entry = json.loads(line)
            status = check_status(entry['html'])
            if status == 'passed':
                features = extract_feats(entry['html'])
                features['id'] = entry['id']
                posts.insert_one(features)
                features_collect.append(features)
                is_exists.append(entry['id'])
                passed_ct += 1
            elif status == 'check':
                check.append(entry['id'])
        ct += 1
        if ct%20 == 0:
            print "check {} records of which {} passed and have been parsed".format(ct, passed_ct)
        json_data.close()
