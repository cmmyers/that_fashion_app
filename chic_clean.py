

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
    title = soup.find("h1", { "class":"photo_title"}).text
    fd['title'] = title
    #find date of post
    date = soup.find("meta", {"itemprop":"dateCreated"}).get("content")
    fd['date'] = date

    #find smaller photos url
    sub_photos = soup.find("div", {"class":"subphoto_items"})
    if sub_photos is not None:
        sub_photos = sub_photos.findChildren("img")
        sub_photos = [photo.get("src") for photo in sub_photos]
        fd['subphotos'] = sub_photos
    else:
        fd['subphotos'] = "n/a"

    #find main photo
    main_photo = soup.find("div", {"id" : "image_wrap"}).findChild("img").get("src")
    fd['main_photo'] = main_photo

    #number of votes for this post
    votes = soup.find("div", {"id": "vote_text_100000"})
    if votes is not None:
        votes = votes.text
        votes = int(votes.split()[0])
        fd['votes'] = votes
    else:
        fd['votes'] = 0

    #number of comments for this post
    comments = soup.find("div", {"id": "comment_text_100000"})
    if comments is not None:
        comments = comments.text
        comments = int(comments.split()[0])
        fd['comments'] = comments
    else:
        fd['comments'] = 0

    #number of favorites for this post
    faves = soup.find("div", {"id": "favorite_text_100000"})
    if faves is not None:
        faves = faves.text
        faves = int(faves.split()[0])
        fd['favorites'] = faves
    else:
        fd['faves'] = 0

    #find all tags
    tags = soup.find("div", {"id": "tag_boxes"}).findChildren("a")
    tags = [tag.text for tag in tags]
    fd['tags'] = tags

    #find description
    desc = soup.find("div", {"id": "photo_description"}).text
    fd['photo_desc'] = desc

    #find links to garments
    links = soup.find("div",{"class": "garmentLinks"})
    fd['garment_links'] = links

    #find styleCouncl status
    style_council = soup.find("div", {"class":"help"}).findChild("img").get("alt")
    fd['style_council'] = style_council

    #find number of followers
    followers = soup.find("div", {"id":"follow"}).text
    fd['followers'] = followers

    #find username
    username = soup.find("div",{ "id":"name_div"}).findChild("a").text
    fd['username'] = username


    #find location
    location = soup.find("div", {"id":"loc_div"}).findChild("a")
    if location is not  None:
        location = location.text
        fd['location'] = location
    else:
        fd['location'] = "n/a"

    #find num chic points
    chic_points = soup.find("div", {"itemprop": "author"}).findChildren("div", {"class":"px10"})[2].text
    chic_points = chic_points.split()[0]
    fd['chic_points'] = chic_points

    ''''''
    return fd

def view_entry():
    with open(path) as json_data:
        for line in json_data:
            print json.loads(line)['html']


if __name__ == '__main__':
    # path = raw_input("Please enter the path to the json file you would like to clean ")
    path = 'chic_export_24.json'
    is_exists = []
    check = []
    features_collect = []
    with open(path) as json_data:
        for line in json_data:
            entry = json.loads(line)
            status = check_status(entry['html'])
            if status == 'passed':
                features = extract_feats(entry['html'])
                features['id'] = entry['id']
                features_collect.append(features)
                is_exists.append(entry['id'])
            elif status == 'check':
                check.append(entry['id'])
        json_data.close()
