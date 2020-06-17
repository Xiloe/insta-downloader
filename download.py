import requests
import json
import re
import os


def download(is_video, shortcode, display_url, username):
    # Make a folder with the name of the owner.
    try:
        if not os.path.exists(username):
            os.makedirs(username)
    except:
        print("An error occured while creating the folder.")

    # Download the image and save it.
    response = requests.get(display_url)

    filetype = "jpg"
    if is_video:
        filetype = "mp4"

    try:
        open(f'{username}/{shortcode}.{filetype}', 'wb').write(response.content)
        print(f"Successfully downloaded {shortcode}")
    except:
        print("An error occured while saving the image")
        exit()


# Headers to appear more hooman. And not really fancy way to input in url.
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
url = 'https://www.instagram.com/graphql/query/?query_hash=8c1ccd0d1cab582bafc9df9f5983e80d&variables={"shortcode":"' + re.findall(r'[A-Za-z0-9-_]{11}', str(input("Post URL: ")))[0] + '","child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":24,"has_threaded_comments":true}'

# Get the json from the response
response = requests.get(url, headers=headers).json()
data = response["data"]["shortcode_media"]

# Exit if post is null or private
if data == None:
    print("The post you tried to download is either invalid or private!")
    exit()

# Get what we need from the post
typename = data["__typename"]
display_url = data["display_url"]
shortcode = data["id"]
is_video = data["is_video"]
owner = data["owner"]
username = owner['username']

if is_video:
    display_url = data["video_url"]

if typename == "GraphSidecar":
    for node in data["edge_sidecar_to_children"]["edges"]:
        node = node["node"]
        display_url = node["display_url"]
        is_video = node["is_video"]
        shortcode = node["id"]
        download(is_video, shortcode, display_url, username)
else:
    download(is_video, shortcode, display_url, username)