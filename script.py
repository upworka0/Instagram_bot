import requests
from pprint import pprint

# set variables for files' path
userpassFilepath = "userpass.txt"
proxiesFilepaht = "proxies.txt"
outputFilepath = "sessonid.txt"

# read file contents
with open(userpassFilepath, "r") as f:
    userpasses = f.readlines()

# open file for output
outputf = open(outputFilepath, "a")

def OutPut(text):
    outputf.write("{}\n".format(text))

def getCSRFToken():
    csrf_Url = "https://www.instagram.com/accounts/login/"
    res = requests.get(csrf_Url)
    csrf_token = res.cookies['csrftoken']
    return csrf_token


def LoginAction(userpassword):
    try:
        user = userpassword.split(":")[0]
        password = userpassword.split(":")[1]
    except:
        password = ""

    url = "https://www.instagram.com/accounts/login/ajax/"
    payload = "username={0}&password={1}".format(user, password)
    headers = {
        # 'cookie': "ig_cb=1; mid=XPmyXwALAAGyaJ6fKF2NNpS8Btdo; fbm_124024574287414=base_domain=.instagram.com; shbid=11282; shbts=1559924848.659384; csrftoken=bRilygvIFbkudi4JuZD6QeGTYQJBRAZg; rur=FTW; urlgen=\"{\\\"37.231.220.117\\\": 47589\\054 \\\"212.129.4.6\\\": 12876\\054 \\\"94.128.90.231\\\": 47589\\054 \\\"94.128.85.88\\\": 47589}:1hbb6M:EwTyrat4lCmfs2kJVWeiJ6EKKmc\"",
        'origin': "https://www.instagram.com",
        'x-instagram-ajax': "516915163258",
        'content-type': "application/x-www-form-urlencoded",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'x-csrftoken': getCSRFToken(),
        'x-ig-app-id': "936619743392459",
        'referer': "https://www.instagram.com/accounts/login/?source=auth_switcher"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    try:
        OutPut(response.cookies['sessionid'])
    except:
        pass

LoginAction(userpasses[0])

outputf.close()