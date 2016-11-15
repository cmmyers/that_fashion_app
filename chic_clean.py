from pymongo import MongoClient
import json
from bs4 import BeautifulSoup


def check_status(html):
    '''some entries either refer to urls with no photo or return an error.
    this function will alert to pages that do not exist and flag pages that should
    rechecked.

    INPUT: unicode object containing unparsed HTML
    OUTPUT: string'''

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
    '''
    '''

    soup = BeautifulSoup(html, "html.parser")
    #features dictionary
    fd = {}

    #find post id for reference
    post_id = soup.find("input", {"id" :"photo_id"})
    if post_id is not None:
        post_id = int(post_id.get("value"))
        fd['post_id'] = post_id
    else:
        fd['post_id'] = 0

    #find title of post
    title = soup.find("h1", { "class":"photo_title"})
    if title is not None:
        title = title.text
        fd['title'] = title.encode('ascii', 'ignore')
    else:
        fd['title'] = 'No Title'

    #find date of post
    date = soup.find("meta", {"itemprop":"dateCreated"})
    if date is not None:
        date = date.get("content")
        fd['date'] = date.encode('ascii', 'ignore')
    else:
        fd['date'] = "No Date"

    #find smaller photos url
    sub_photos = soup.find("div", {"class":"subphoto_items"})
    if sub_photos is not None:
        sub_photos = sub_photos.findChildren("img")
        sub_photos = [photo.get("src") for photo in sub_photos]
        fd['subphotos'] = sub_photos
    else:
        fd['subphotos'] = "No Subphotos"

    #find main photo
    main_photo = soup.find("div", {"id" : "image_wrap"})
    if main_photo is not None:
        main_photo = main_photo.findChild("img").get("src")
        fd['main_photo'] = main_photo.encode("ascii", "ignore")
    else:
        fd['main_photo'] = "No Main Photo"

    #number of votes for this post
    vote_tag = "vote_text_{}".format(post_id)
    votes = soup.find("div", {"id": vote_tag})
    if votes is not None:
        votes = votes.text
        votes = int(votes.split()[0])
        fd['votes'] = int(votes)
    else:
        fd['votes'] = 0

    #number of comments for this post
    comments_tag = "comment_text_{}".format(post_id)
    comments = soup.find("div", {"id": comments_tag})
    if comments is not None:
        comments = comments.text
        comments = int(comments.split()[0])
        fd['comments'] = int(comments)
    else:
        fd['comments'] = 0

    #number of favorites for this post
    faves_tag = "favorite_text_{}".format(post_id)
    faves = soup.find("div", {"id": faves_tag})
    if faves is not None:
        faves = faves.text
        faves = int(faves.split()[0])
        fd['favorites'] = int(faves)
    else:
        fd['favorites'] = 0

    #find all tags
    tags = soup.find("div", {"id": "tag_boxes"})
    if tags is not None:
        tags = tags.findChildren("a")
        tags = [tag.text.encode('ascii', 'ignore') for tag in tags]
        fd['tags'] = tags
    else:
        fd['tags'] = "No Tags"

    #find description
    desc = soup.find("div", {"id": "photo_description"})
    if desc is not None:
        desc = desc.text
        fd['photo_desc'] = desc.encode('ascii', 'ignore')
    else:
        fd['photo_desc'] = "No Description"

    #find links to garments
    links = soup.find("div",{"class": "garmentLinks"})
    if links is not None:
        links = links.findChildren("a")
        fd['garment_links'] = [link.text.encode('ascii', 'ignore') for link in links]
    else:
        fd['garment_links'] = None

    #find styleCouncl status
    style_council = soup.find("div", {"class":"help"})
    if style_council is not None:
        style_council = style_council.findChild("img").get("alt")
        fd['style_council'] = style_council.encode('ascii', 'ignore')
    else:
        fd['style_council'] = "Not Style Council (or..no badge?)"

    #find number of followers
    followers = soup.find("div", {"id":"fan_count"})
    if followers is not None:
        followers = followers.text
        if followers != '\n\n':
            fd['followers'] = int(followers)
    else:
        fd['followers'] = 0

    fd['followers']

    #find username
    username = soup.find("div",{ "id":"name_div"})
    if username is not None:
        username = username.findChild("a").text
        fd['username'] = username.encode('ascii', 'ignore')
    else:
        fd['username'] = "No Username"


    #find location
    location = soup.find("div", {"id":"loc_div"})
    if location is not None:
        location = location.findChild("a")
        if location is not None:
            location = location.text
            fd['location'] = location.encode('ascii', 'ignore')
    else:
        fd['location'] = "n/a"

    #find num chic points
    chic_points = soup.find("div", {"itemprop": "author"})
    if chic_points is not None:
        chic_points = chic_points.findChildren("div", {"class":"px10"})[2].text
        chic_points = chic_points.split()[0]
        fd['chic_points'] = int(chic_points)
    else:
        fd['chic_points'] = 0

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
    db = client['parsedA']
    print "Using database {}".format(db)
    #db_name = raw_input("Database name: ")
    collection = raw_input("Collection name: ")


    posts = db[collection]

    ct = 1
    passed_ct = 0
    with open(path) as json_data:
        for line in json_data:
            if ct > 1040:
                entry = json.loads(line)
                status = check_status(entry['html'])
                if status == 'passed':
                    features = extract_feats(entry['html'])
                    features['id'] = int(entry['id'])
                    posts.insert_one(features)
                    features_collect.append(features)
                    is_exists.append(entry['id'])
                    passed_ct += 1
                elif status == 'check':
                    check.append(entry['id'])
            ct += 1
            if ct%20 == 0:
                print "checked {} records of which {} passed and have been parsed".format(ct, passed_ct)
            if passed_ct == 1000:
                break
        json_data.close()
